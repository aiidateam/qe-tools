"""Output of the Quantum ESPRESSO pw.x code."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from qe_tools.outputs.base import BaseOutput

from .parsers.base import BaseStdoutParser
from .parsers.dos import DosParser
from .parsers.pw import PwXMLParser


def _determine_spin_type(spin: dict) -> str:
    if spin["noncolin"]:
        return "non-collinear"
    if spin["spinorbit"]:
        return "spin-orbit"
    if spin["lsda"]:
        return "spin-polarised"
    return "non-spin-polarised"


class DosOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

    _output_spec_mapping = {
        "energy": "dos.energy",
        "dos": "dos.dos",
        "dos_up": "dos.dos_up",
        "dos_down": "dos.dos_down",
        "fermi_energy": "dos.fermi_energy",
        "integrated_dos": "dos.integrated_dos",
        "full_dos": "dos",
        "spin_type": ("xml.input.spin", _determine_spin_type),
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
        dos_file = next(directory.glob("*.dos"), None)
        xml_file = next(directory.rglob("data-file*.xml"), None)

        for file in [path for path in directory.iterdir() if path.is_file()]:
            with file.open("r") as handle:
                header = "".join(handle.readlines(5))

                if "Program DOS" in header:
                    stdout_file = file

        return cls.from_files(dos=dos_file, xml=xml_file, stdout=stdout_file)

    @classmethod
    def from_files(
        cls,
        *,
        dos: None | str | Path | TextIO = None,
        xml: None | str | Path | TextIO = None,
        stdout: None | str | Path | TextIO = None,
    ):
        """Parse the outputs directly from the provided files."""
        raw_outputs = {}

        if stdout is not None:
            raw_outputs["stdout"] = BaseStdoutParser.parse_from_file(stdout)

        if dos is not None:
            raw_outputs["dos"] = DosParser.parse_from_file(dos)

        if xml is not None:
            raw_outputs["xml"] = PwXMLParser.parse_from_file(xml)

        return cls(raw_outputs=raw_outputs)
