"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations
from glom import glom

import abc

from qe_tools.converters.base import BaseConverter


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

    def list_outputs(self) -> list[str]:
        """List the available outputs."""
        return list(BaseConverter.output_mapping.keys())
