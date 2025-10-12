"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations
from functools import cached_property
from types import SimpleNamespace
from glom import glom, GlomError

import abc


class BaseOutput(abc.ABC):
    """
    Abstract class for the outputs of Quantum ESPRESSO.
    """

    def __init__(self, raw_outputs: dict):
        self.raw_outputs = raw_outputs

    @classmethod
    @abc.abstractmethod
    def from_dir(cls, directory: str):
        pass

    def get_output_from_spec(self, spec):
        """Extract data from the "raw" outputs using a `glom` specification."""
        return glom(self.raw_outputs, spec)

    def get_output(self, name: str, to=None):
        """Return a parsed output by key, optionally converted to a library object.

        Args:
            name (str): Output key to retrieve (e.g., 'structure', 'fermi_energy',
                'forces').
            to (str | None): Optional target library to convert the base output to. One
                of {'aiida', 'ase', 'pymatgen'}.

        Examples:
            >>> parser.get_output(name="structure")
            >>> parser.get_output(name="structure", to="pymatgen")
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
        self, names: None | list[str] = None, to: None | str = None
    ) -> dict:
        """Return a dictionary of (selected) outputs.

        Args:
            names (list[str]): Output names to include.
            to (str): Convert each output to a target library (e.g., "aiida", "ase",
                "pymatgen").

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
    def outputs(self) -> SimpleNamespace:
        """Namespace with successfully retrievable outputs."""
        namespace = SimpleNamespace()

        for name in self.list_outputs(only_available=True):
            setattr(namespace, name, self.get_output(name))

        return namespace
