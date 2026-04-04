"""Abstract base class for the outputs of Quantum ESPRESSO."""

from __future__ import annotations

import abc
import dataclasses
import typing
from functools import cached_property

from glom import glom, GlomError, Spec


T = typing.TypeVar("T")


def output_mapping(cls):
    """Decorator that defines a typed, frozen output mapping for a Quantum ESPRESSO code.

    Applies `@dataclass(frozen=True)` and injects `__getattribute__` and `__dir__` so that:

    - Accessing a field whose value is still a `Spec` raises `AttributeError` with a clear
      message (i.e. the output was not parsed).
    - `dir()` only lists fields that were successfully extracted.

    Each field must declare a `Spec(...)` as its default value:

        fermi_energy: float = Spec("path.to.fermi_energy")
        \"""Fermi energy in eV.\"""
    """

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if isinstance(value, Spec):
            raise AttributeError(f"'{name}' is not available in the parsed outputs.")
        return value

    def __dir__(self):
        return [
            name for name, value in self.__dict__.items() if not isinstance(value, Spec)
        ]

    cls.__getattribute__ = __getattribute__
    cls.__dir__ = __dir__
    return dataclasses.dataclass(frozen=True)(cls)


class BaseOutput(abc.ABC, typing.Generic[T]):
    """Abstract base class for the outputs of Quantum ESPRESSO."""

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
        self._output_spec_mapping = {}

        for field in dataclasses.fields(self._get_mapping_class()):
            if not isinstance(field.default, Spec):
                raise TypeError(
                    f"{type(self).__name__}.{field.name}: expected a Spec(...) default, "
                    f"got {field.default!r}"
                )
            self._output_spec_mapping[field.name] = field.default

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

    def get_output(
        self, name: str, to: typing.Literal["aiida", "ase", "pymatgen"] | None = None
    ):
        """Return an output by `name`.

        Args:
            name (str): Output to retrieve (e.g., "structure", "fermi_energy",
                "forces").
            to (str): Optional target library to convert the base output to. One of
                "aiida", "ase", "pymatgen".

        Examples:
            >>> pw_out.get_output(name="structure")
            >>> pw_out.get_output(name="structure", to="pymatgen")
        """
        output_data = glom(self.raw_outputs, self._output_spec_mapping[name])

        if to is None:
            return output_data

        if to == "aiida":
            from qe_tools.converters.aiida import AiiDAConverter as Converter
        elif to == "ase":
            from qe_tools.converters.ase import ASEConverter as Converter
        elif to == "pymatgen":
            from qe_tools.converters.pymatgen import PymatgenConverter as Converter
        else:
            raise ValueError(f"Library '{to}' is not supported.")

        return (
            Converter().convert(name, output_data)
            if name in Converter.conversion_mapping
            else output_data
        )

    def get_output_dict(
        self,
        names: None | list[str] = None,
        to: typing.Literal["aiida", "ase", "pymatgen"] | None = None,
    ) -> dict:
        """Return a dictionary of outputs.

        Args:
            names (list[str]): Output names to include. If not provided, all
                available outputs are included.
            to (str): Optional target library to convert each output to. One of
                "aiida", "ase", "pymatgen".

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
        return self._get_mapping_class()(**self.get_output_dict())
