"""Base parser for Quantum ESPRESSO stdout files."""

from __future__ import annotations

import re

from dough.outputs import BaseOutputFileParser

from qe_tools.utils import convert_qe_time_to_sec


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
