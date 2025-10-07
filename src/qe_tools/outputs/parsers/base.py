"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations

import abc
import re
from io import TextIOBase
from pathlib import Path
from typing import TextIO

from qe_tools.utils import convert_qe_time_to_sec


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for the parsing of output files of Quantum ESPRESSO.
    Each parser should parse a single file.
    A computation with multiple files as outputs (e.g., NEB)
    should therefore require multiple parsers.
    """

    @staticmethod
    @abc.abstractmethod
    def parse(content: str):
        """
        Parse the output of Quantum ESPRESSO.
        This should be implemented for XML and standard output,
        whenever possible, in dedicated objects
        (e.g., PwStdoutParser and PwXMLParser).
        """

    @classmethod
    def parse_from_file(cls, file: str | Path | TextIO):
        """
        Helper function to generate a BaseOutputFileParser object
        from a file instead of its string.
        """
        if isinstance(file, (str, Path)):
            with Path(file).open("r") as handle:
                content = handle.read()
        elif isinstance(file, TextIOBase):
            content = file.read()
        else:
            raise TypeError(f"Unsupported type: {type(file)}")

        return cls.parse(content)


class BaseStdoutParser(BaseOutputFileParser):
    """Abstract class for the parsing of stdout files of Quantum ESPRESSO."""

    @staticmethod
    def parse(content):
        """Parse the basic ``stdout`` content of a Quantum ESPRESSO calculation.

        This function only checks for basic content like the code name and version,
        as well as the wall time of the calculation.

        :returns: dictionary of the parsed data.
        """
        parsed_data = {}

        code_match = re.search(
            r"Program\s(?P<code_name>[A-Za-z\_\d]+)\sv\.(?P<code_version>[\d\.a-zA-Z]+)\s",
            content,
        )
        if code_match:
            code_name = code_match.groupdict()["code_name"]
            parsed_data["code_version"] = code_match.groupdict()["code_version"]

            wall_match = re.search(
                rf"{code_name}\s+:[\s\S]+CPU\s+(?P<wall_time>[\s.\dsmdh]+)\sWALL",
                content,
            )
            if wall_match:
                parsed_data["wall_time_seconds"] = convert_qe_time_to_sec(
                    wall_match.groupdict()["wall_time"]
                )

        return parsed_data
