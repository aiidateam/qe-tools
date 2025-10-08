"""Output of the Quantum ESPRESSO pw.x code."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from qe_tools.outputs.base import BaseOutput
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser

from qe_tools import CONSTANTS


class PwOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

    _output_spec_mapping = {
        "structure": {
            "atomic_species": (
                "xml.output.atomic_species.species",
                [lambda species: species["@name"]],
            ),
            "cell": (
                "xml.output.atomic_structure.cell",
                lambda cell: [
                    [coord * CONSTANTS.bohr_to_ang for coord in cell["a1"]],
                    [coord * CONSTANTS.bohr_to_ang for coord in cell["a2"]],
                    [coord * CONSTANTS.bohr_to_ang for coord in cell["a3"]],
                ],
            ),
            "symbols": (
                "xml.output.atomic_structure.atomic_positions.atom",
                [lambda atom: atom["@name"]],
            ),
            "positions": (
                "xml.output.atomic_structure.atomic_positions.atom",
                [
                    lambda atom: [
                        CONSTANTS.bohr_to_ang * position for position in atom["$"]
                    ]
                ],
            ),
        },
        "fermi_energy": "xml.output.band_structure.fermi_energy",
    }

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
            raw_outputs["stdout"] = PwStdoutParser.parse_from_file(stdout)

        if xml is not None:
            raw_outputs["xml"] = PwXMLParser.parse_from_file(xml)

        return cls(raw_outputs=raw_outputs)
