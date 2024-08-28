# -*- coding: utf-8 -*-
"""Base parser for the outputs of Quantum ESPRESSO."""

import abc
from pathlib import Path


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for the parsing of output files of Quantum ESPRESSO.
    """

    def __init__(self, raw_data: dict | None = None):
        self.raw_data = raw_data or {}

    @abc.abstractmethod
    def parse_stdout(self, output_file):
        """Parse the standard output of Quantum ESPRESSO."""
        pass

    @abc.abstractmethod
    def parse_xml(self, xml_file):
        """Parse the XML output of Quantum ESPRESSO."""
        pass

    @classmethod
    def from_dir(cls, directory: str | Path):
        pass
