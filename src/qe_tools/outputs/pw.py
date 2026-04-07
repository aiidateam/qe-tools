"""Output of the Quantum ESPRESSO pw.x code."""

import math
from pathlib import Path
from typing import TextIO

from glom import Coalesce, Spec

from qe_tools.outputs.base import BaseOutput, output_mapping
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser

from qe_tools import CONSTANTS


@output_mapping
class _PwMapping:
    """Typed outputs of a pw.x calculation."""

    structure: dict = Spec(
        {
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
        }
    )
    """Crystal structure: cell vectors (Å), element symbols, and Cartesian positions (Å)."""

    forces: list = Spec(
        (
            "xml.output.forces",
            lambda forces: [
                [
                    value * CONSTANTS.hartree_to_ev / CONSTANTS.bohr_to_ang
                    for value in forces["$"][atom_index * 3 : (atom_index + 1) * 3]
                ]
                for atom_index in range(forces["@dims"][1])
            ],
        )
    )
    """Forces on atoms in eV/Å, shape [n_atoms][3]."""

    stress: list = Spec(
        (
            "xml.output.stress",
            lambda stress: [
                [
                    value * CONSTANTS.au_gpa
                    for value in stress["$"][row_number * 3 : (row_number + 1) * 3]
                ]
                for row_number in range(3)
            ],
        )
    )
    """Stress tensor in GPa, shape [3][3]."""

    fermi_energy: float = Spec(
        (
            "xml.output.band_structure.fermi_energy",
            lambda energy: energy * CONSTANTS.hartree_to_ev,
        )
    )
    """Fermi energy in eV."""

    fermi_energy_up: float = Spec(
        (
            "xml.output.band_structure.two_fermi_energies",
            lambda energies: energies[0] * CONSTANTS.hartree_to_ev,
        )
    )
    """Fermi energy of spin-up channel in eV.
    
    Only available when ``tot_magnetization`` is set in ``SYSTEM``.
    """

    fermi_energy_down: float = Spec(
        (
            "xml.output.band_structure.two_fermi_energies",
            lambda energies: energies[1] * CONSTANTS.hartree_to_ev,
        )
    )
    """Fermi energy of spin-down channel in eV.
    
    Only available when ``tot_magnetization`` is set in ``SYSTEM``.
    """

    number_of_k_points: int = Spec("xml.output.band_structure.nks")
    """Number of k-points at which the Kohn-Sham states were computed."""

    k_points_weights: list = Spec(
        (
            "xml.output.band_structure.ks_energies",
            [lambda ks: ks["k_point"]["@weight"]],
        )
    )
    """Weights of the k-points at which the Kohn-Sham states were computed.

    Dimensionless; per QE convention the weights sum to 2 for `nspin=1` and to 1 for `nspin=2`.
    """

    k_points_cartesian: list = Spec(
        (
            "xml.output",
            lambda output: [
                [
                    kp
                    * 2
                    * math.pi
                    / (output["atomic_structure"]["@alat"] * CONSTANTS.bohr_to_ang)
                    for kp in ks["k_point"]["$"]
                ]
                for ks in output["band_structure"]["ks_energies"]
            ],
        )
    )
    """Cartesian coordinates of the k-points in 1/Å, shape `[n_kpoints][3]`."""

    number_of_bands: int = Spec(
        Coalesce(
            "xml.output.band_structure.nbnd",
            "xml.output.band_structure.nbnd_up",
        )
    )
    """Number of Kohn-Sham bands (per spin channel for spin-polarized calculations)."""

    total_energy: float = Spec(
        (
            "xml.output.total_energy.etot",
            lambda energy: energy * CONSTANTS.hartree_to_ev,
        )
    )
    """Total energy in eV."""


class PwOutput(BaseOutput[_PwMapping]):
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
        xml_file = next(directory.rglob("data-file*.xml"), None)

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
