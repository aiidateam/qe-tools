"""Abstract base class for the outputs of Quantum ESPRESSO."""

from __future__ import annotations

import abc
import contextlib
import dataclasses
import typing
from functools import cached_property

from glom import glom, GlomError, Spec

from qe_tools.converters.base import BaseConverter


T = typing.TypeVar("T")


class SubMapping:
    """Sentinel marking a field as a nested output mapping.

    `BaseOutput` resolves these at instantiation time. Nesting is intended to
    be one level only: a sub-mapping class should only contain `Spec` fields.
    """

    def __init__(self, mapping_cls: type):
        self.mapping_cls = mapping_cls


def output_mapping(cls):
    """Decorator that defines a typed, frozen output mapping for a Quantum ESPRESSO code.

    Applies `@dataclass(frozen=True)` and injects `__getattribute__` and `__dir__` so that:

    - Accessing a field whose value is still a `Spec` or `SubMapping` raises
      `AttributeError` with a clear message (i.e. the output was not parsed).
    - `dir()` only lists fields that were successfully extracted.

    Output fields declare a `Spec(...)` default. Sub-namespace fields are
    declared with a bare annotation whose type is another `@output_mapping`
    class — the decorator auto-injects a `SubMapping(hint)` default:

        fermi_energy: float = Spec("path.to.fermi_energy")
        \"""Fermi energy in eV.\"""
        magnetization: _MagnetizationMapping
        \"""Nested magnetization outputs.\"""
    """

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if isinstance(value, (Spec, SubMapping)):
            raise AttributeError(f"'{name}' is not available in the parsed outputs.")
        return value

    def __dir__(self):
        return [
            name
            for name, value in self.__dict__.items()
            if not isinstance(value, (Spec, SubMapping))
        ]

    cls.__getattribute__ = __getattribute__
    cls.__dir__ = __dir__

    # Inject `SubMapping(hint)` defaults for bare annotations whose type is
    # itself an `@output_mapping`-decorated class. Note: `get_type_hints`
    # evaluates annotations, which is fine as long as the module does not use
    # `from __future__ import annotations` together with `TYPE_CHECKING`-only
    # sub-mapping imports — in that case the eval would raise `NameError` here.
    # Sub-mapping classes must be defined *before* the parent that references
    # them (Python enforces this anyway for non-future-annotations modules).
    for name, hint in typing.get_type_hints(cls).items():
        if hasattr(cls, name):  # already has a default
            continue

        if not (isinstance(hint, type) and getattr(hint, "_is_output_mapping", False)):
            raise TypeError(
                f"{cls.__name__}.{name}: needs a Spec(...) default, or a bare "
                f"annotation whose type is an @output_mapping class "
                f"(which must be defined before this class)"
            )

        setattr(cls, name, SubMapping(hint))

    cls._is_output_mapping = True
    return dataclasses.dataclass(frozen=True)(cls)


class BaseOutput(abc.ABC, typing.Generic[T]):
    """Abstract base class for the outputs of Quantum ESPRESSO."""

    converters: typing.ClassVar[dict[str, type[BaseConverter]]] = {}
    """Mapping of target-library name to its `BaseConverter` subclass.

    Subclasses populate this with the converters they support, e.g.

        `converters = {"ase": ASEConverter, ...}`

    Each converter is responsible for importing optional dependencies lazily inside the
    `get_conversion_mapping()` classmethod, so simply listing it here does not pull it
    in at import time.
    """

    @classmethod
    def _get_mapping_class(cls) -> type:
        """Extract the mapping class from the generic parameter.

        Example: PwOutput(BaseOutput[_PwMapping]) → _PwMapping
        """
        for base in getattr(cls, "__orig_bases__", []):
            if typing.get_origin(base) is BaseOutput and (
                args := typing.get_args(base)
            ):
                return args[0]
        raise TypeError(
            f"{cls.__name__} must subclass BaseOutput[T] with a decorated output mapping, "
            "e.g. class PwOutput(BaseOutput[_PwMapping])"
        )

    def __init__(self, raw_outputs: dict):
        self.raw_outputs = raw_outputs

        def build(mapping_cls: type) -> dict:
            """Build the nested spec dict from a mapping class."""
            result: dict = {}

            for field in dataclasses.fields(mapping_cls):
                if isinstance(field.default, SubMapping):
                    result[field.name] = build(field.default.mapping_cls)
                elif isinstance(field.default, Spec):
                    result[field.name] = field.default
                else:
                    raise TypeError(
                        f"{mapping_cls.__name__}.{field.name}: expected a Spec(...) or "
                        f"SubMapping(...) default, got {field.default!r}"
                    )

            return result

        self._output_spec_mapping = build(self._get_mapping_class())

    @classmethod
    @abc.abstractmethod
    def from_dir(cls, directory: str):
        pass

    def get_output_from_spec(self, spec):
        """Return a value from `raw_outputs` using a glom specification.

        Args:
            spec: A glom specification describing the path/transforms to apply.

        Raises:
            GlomError: If the specification is invalid or the path cannot be resolved.
        """
        return glom(self.raw_outputs, spec)

    def get_output(self, name: str, to: str | None = None):
        """Return an output by `name`.

        Args:
            name (str): Output to retrieve (e.g., "structure", "fermi_energy",
                "forces").
            to (str): Optional target library to convert the base output to.

                The supported values are the keys of this subclass's `converters`
                class variable — list them with

                    `sorted(OutputClass.converters)`

                Passing an unsupported value raises `ValueError` listing the
                available options.

        Examples:
            >>> pw_out.get_output(name="structure")
            >>> pw_out.get_output(name="structure", to="pymatgen")
        """
        entry = self._output_spec_mapping[name]

        if isinstance(entry, dict):
            output_data: typing.Any = {}

            for sub_name, sub_spec in entry.items():
                with contextlib.suppress(GlomError):
                    output_data[sub_name] = glom(self.raw_outputs, sub_spec)
        else:
            output_data = glom(self.raw_outputs, entry)

        if to is None:
            return output_data

        try:
            Converter = self.converters[to]
        except KeyError:
            available = sorted(self.converters)
            raise ValueError(
                f"Library '{to}' is not supported. Available: {available}"
            ) from None

        conversion_mapping = Converter.get_conversion_mapping()

        if isinstance(entry, dict):
            return {
                sub_name: Converter().convert(f"{name}.{sub_name}", sub_value)
                if sub_name in conversion_mapping
                else sub_value
                for sub_name, sub_value in output_data.items()
            }

        return (
            Converter().convert(name, output_data)
            if name in conversion_mapping
            else output_data
        )

    def get_output_dict(
        self,
        names: None | list[str] = None,
        to: str | None = None,
    ) -> dict:
        """Return a dictionary of outputs.

        Args:
            names (list[str]): Output names to include. If not provided, all
                available outputs are included.
            to (str): Optional target library to convert the base output to.

                The supported values are the keys of this subclass's `converters`
                class variable — list them with

                    `sorted(OutputClass.converters)`

                Passing an unsupported value raises `ValueError` listing the
                available options.

        Returns:
            dict: Mapping from output name to value.
        """
        names = names or self.list_outputs()
        return {name: self.get_output(name, to=to) for name in names}

    def list_outputs(self, only_available: bool = True) -> list[str]:
        """List the output names.

        Args:
            only_available (bool, default True): Include only outputs that are
                available, i.e. produced by the calculation and successfully parsed. If
                False, list all outputs that this parser supports.

        Returns:
            list[str]: A list of output names.
        """
        if not only_available:
            return list(self._output_spec_mapping.keys())

        output_names = []

        for name in self._output_spec_mapping.keys():
            try:
                self.get_output(name)
            except GlomError:
                continue
            else:
                output_names.append(name)

        return output_names

    @cached_property
    def outputs(self) -> T:
        """Namespace with available outputs."""

        def build(mapping_cls: type, data: dict):
            defaults = {f.name: f.default for f in dataclasses.fields(mapping_cls)}
            kwargs = {
                name: build(defaults[name].mapping_cls, value)  # type: ignore[union-attr]
                if isinstance(defaults[name], SubMapping)
                else value
                for name, value in data.items()
            }
            return mapping_cls(**kwargs)

        return build(self._get_mapping_class(), self.get_output_dict())
