"""Output of the Quantum ESPRESSO pw.x code."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from qe_tools.outputs.base import BaseOutput
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser


class PwOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

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
        xml_file = next(directory.rglob("data-file*.xml"))

        for file in [path for path in directory.iterdir() if path.is_file()]:
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
        raw_outputs = {}

        if stdout is not None:
            parser_std = PwStdoutParser.from_file(stdout)
            parser_std.parse()
            raw_outputs |= parser_std.dict_out

        if xml is not None:
            parser_xml = PwXMLParser.from_file(xml)
            parser_xml.parse()
            raw_outputs |= parser_xml.dict_out

        return cls(raw_outputs=raw_outputs)

    def get_output(self, output: str, fmt="basic"):
        if fmt == "basic":
            from qe_tools.converters.base import BaseConverter

            return BaseConverter().get_output(output, self.raw_outputs)

        if fmt == "aiida":
            from qe_tools.converters.aiida import AiiDAConverter

            return AiiDAConverter().get_output(output, self.raw_outputs)

        if fmt == "ase":
            from qe_tools.converters.ase import ASEConverter

            return ASEConverter().get_output(output, self.raw_outputs)

        if fmt == "pymatgen":
            from qe_tools.converters.pymatgen import PymatgenConverter

            return PymatgenConverter().get_output(output, self.raw_outputs)

        raise ValueError(f"Format '{fmt}' is not supported.")
