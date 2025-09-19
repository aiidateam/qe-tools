"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations

import abc
import re

from qe_tools.utils import convert_qe_time_to_sec


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for the parsing of output files of Quantum ESPRESSO.
    Each parser should parse a single file.
    A computation with multiple files as outputs (e.g., NEB)
    should therefore require multiple parsers.
    """

    def __init__(self, string: str):
        self.string = string
        self.dict_out: dict = {}

    @abc.abstractmethod
    def parse(self):
        """
        Parse the output of Quantum ESPRESSO.
        This should be implemented for XML and standard output,
        whenever possible, in dedicated objects
        (e.g., PwStdoutParser and PwXMLParser).
        """

    @classmethod
    def from_file(cls, filename: str):
        """
        Helper function to generate a BaseOutputFileParser object
        from a file instead of its string.
        """
        with open(filename) as f:
            string = f.read()

        return cls(string=string)


class BaseStdoutParser(BaseOutputFileParser):
    """Abstract class for the parsing of stdout files of Quantum ESPRESSO."""

    def parse(self):
        """Parse the ``stdout`` content of a Quantum ESPRESSO calculation.

        This function only checks for basic content like the code name and version,
        as well as the wall time of the calculation.

        :returns: dictionary of the parsed data.
        """
        parsed_data = {}

        code_match = re.search(
            r"Program\s(?P<code_name>[A-Z|a-z|\_|\d]+)\sv\.(?P<code_version>[\d\.|a-z|A-Z]+)\s", self.string
        )
        if code_match:
            code_name = code_match.groupdict()["code_name"]
            parsed_data["code_version"] = code_match.groupdict()["code_version"]

            wall_match = re.search(rf"{code_name}\s+:[\s\S]+CPU\s+(?P<wall_time>[\s.\d|s|m|d|h]+)\sWALL", self.string)

            if wall_match:
                parsed_data["wall_time_seconds"] = convert_qe_time_to_sec(wall_match.groupdict()["wall_time"])

        self.dict_out |= parsed_data
