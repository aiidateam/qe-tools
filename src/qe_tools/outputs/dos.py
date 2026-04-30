"""Output of the Quantum ESPRESSO dos.x code."""

import typing
from pathlib import Path
from typing import Annotated, TextIO

from glom import Spec

from dough import Unit
from dough.converters import BaseConverter
from dough.outputs import BaseOutput, output_mapping

from qe_tools.converters.aiida import AiiDAConverter
from qe_tools.converters.ase import ASEConverter
from qe_tools.converters.pymatgen import PymatgenConverter

from .parsers.stdout import BaseStdoutParser
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

    energy: Annotated[list, Spec("dos.energy"), Unit("eV")]
    """Energy grid in eV."""

    dos: Annotated[list, Spec("dos.dos"), Unit("1/eV")]
    """Total density of states (states/eV). Not available for spin-polarised calculations."""

    dos_up: Annotated[list, Spec("dos.dos_up"), Unit("1/eV")]
    """Spin-up DOS (states/eV). Not available for non-spin-polarised calculations."""

    dos_down: Annotated[list, Spec("dos.dos_down"), Unit("1/eV")]
    """Spin-down DOS (states/eV). Not available for non-spin-polarised calculations."""

    fermi_energy: Annotated[float, Spec("dos.fermi_energy"), Unit("eV")]
    """Fermi energy in eV."""

    integrated_dos: Annotated[list, Spec("dos.integrated_dos")]
    """Integrated DOS (# of states)."""

    full_dos: Annotated[dict, Spec("dos")]
    """Full parsed DOS dictionary."""

    spin_type: Annotated[str, Spec(("xml.input.spin", _determine_spin_type))]
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
