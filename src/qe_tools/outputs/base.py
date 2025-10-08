"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations
from glom import glom

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

    @classmethod
    def list_outputs(cls) -> list[str]:
        """List the available outputs."""
        return list(cls._output_spec_mapping.keys())

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

        return Converter().convert(name, output_data)
