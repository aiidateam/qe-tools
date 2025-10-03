"""Output of the Quantum ESPRESSO pw.x code."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from qe_tools.outputs.base import BaseOutput
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser


class PwOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

    def __init__(self, outputs: dict | None = None):
        super().__init__(outputs=outputs)

    @classmethod
    def from_dir(cls, directory: str | Path):
        """
        From a directory, locates the standard output and XML files and
        parses them.
        """
        directory = Path(directory)

        if not directory.is_dir():
            raise ValueError(f"Path `{directory}` is not a valid directory.")

        stdout_file = None
        xml_file = None

        for file in [path for path in directory.iterdir() if path.is_file()]:
            if file.suffix == ".xml":
                xml_file = file

            with file.open("r") as handle:
                header = "".join(handle.readlines(5))

                if "Program PWSCF" in header:
                    stdout_file = file

        return cls.from_files(xml=xml_file, stdout=stdout_file)

    @classmethod
    def from_files(
        cls,
        *,
        xml: None | str | Path | TextIO = None,
        stdout: None | str | Path | TextIO = None,
    ):
        """Parse the outputs directly from the provided files."""
        outputs = {}

        if stdout is not None:
            parser_std = PwStdoutParser.from_file(stdout)
            parser_std.parse()
            outputs |= parser_std.dict_out

        if xml is not None:
            parser_xml = PwXMLParser.from_file(xml)
            parser_xml.parse()
            outputs |= parser_xml.dict_out

        return cls(outputs=outputs)
