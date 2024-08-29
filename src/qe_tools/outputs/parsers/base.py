# -*- coding: utf-8 -*-
"""Base parser for the outputs of Quantum ESPRESSO."""

import abc


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for the parsing of output files of Quantum ESPRESSO.
    Each parser should parse a single file.
    A computation with multiple files as outputs (e.g., NEB)
    should therefore require multiple parsers.
    """

    def __init__(self, string: str | None = None):
        self.string = string
        self.dict_out: dict = {}

    @abc.abstractmethod
    def parse(self, *args, **kwargs):
        """
        Parse the output of Quantum ESPRESSO.
        This should be implemented for XML and standard output,
        whenever possible, in dedicated objects
        (e.g., PwStdoutParser and PwXMLParser).
        """
        pass

    @classmethod
    def from_file(cls, filename: str):
        """
        Helper function to generate a BaseOutputFileParser object
        from a file instead of its string.
        """
        with open(filename, 'r') as f:
            string = f.read()

        return cls(string=string)
