"""Base parser for Quantum ESPRESSO stdout files."""

from __future__ import annotations

import re

from dough.outputs import BaseOutputFileParser

from qe_tools.utils import convert_qe_time_to_sec


_VOLUME_RE = re.compile(
    r"unit-cell volume\s*=\s*([\-\d.E+]+)\s*(?:\(a\.u\.\)|a\.u\.)\^3"
)


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

        # Initial line: `unit-cell volume          =     275.9279 (a.u.)^3`.
        # vc-relax also prints `new unit-cell volume = ... a.u.^3 (...)` per step;
        # take the last match so the final cell volume wins.
        volume_matches = _VOLUME_RE.findall(content)
        if volume_matches:
            parsed_data["volume_bohr3"] = float(volume_matches[-1])

        return parsed_data
