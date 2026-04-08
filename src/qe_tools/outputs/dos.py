"""Output of the Quantum ESPRESSO dos.x code."""

import typing
from pathlib import Path
from typing import TextIO

from glom import Spec

from qe_tools.converters.aiida import AiiDAConverter
from qe_tools.converters.ase import ASEConverter
from qe_tools.converters.base import BaseConverter
from qe_tools.converters.pymatgen import PymatgenConverter
from qe_tools.outputs.base import BaseOutput, output_mapping

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


@output_mapping
class _DosMapping:
    """Typed outputs of a dos.x calculation."""

    energy: list = Spec("dos.energy")
    """Energy grid in eV."""

    dos: list = Spec("dos.dos")
    """Total density of states (states/eV). Not available for spin-polarised calculations."""

    dos_up: list = Spec("dos.dos_up")
    """Spin-up DOS (states/eV). Not available for non-spin-polarised calculations."""

    dos_down: list = Spec("dos.dos_down")
    """Spin-down DOS (states/eV). Not available for non-spin-polarised calculations."""

    fermi_energy: float = Spec("dos.fermi_energy")
    """Fermi energy in eV."""

    integrated_dos: list = Spec("dos.integrated_dos")
    """Integrated DOS."""

    full_dos: dict = Spec("dos")
    """Full parsed DOS dictionary."""

    spin_type: str = Spec(("xml.input.spin", _determine_spin_type))
    """Spin type: 'non-spin-polarised', 'spin-polarised', 'non-collinear', or 'spin-orbit'."""


class DosOutput(BaseOutput[_DosMapping]):
    """Output of the Quantum ESPRESSO dos.x code."""

    converters: typing.ClassVar[dict[str, type[BaseConverter]]] = {
        "ase": ASEConverter,
        "pymatgen": PymatgenConverter,
        "aiida": AiiDAConverter,
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
