"""Output of the Quantum ESPRESSO pw.x code."""

import math
import typing
from pathlib import Path
from typing import Annotated, TextIO

from glom import Coalesce, Spec

from dough import Unit
from dough.converters import BaseConverter
from dough.outputs import BaseOutput, output_mapping

from qe_tools.converters.aiida import AiiDAConverter
from qe_tools.converters.ase import ASEConverter
from qe_tools.converters.pymatgen import PymatgenConverter
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser

from qe_tools import CONSTANTS


@output_mapping
class _PwParametersMapping:
    """Parameters the pw.x calculation ran with.

    Includes both user-supplied inputs (cutoffs, k-points, smearing, ...) and values
    resolved by QE at runtime (effective FFT grids, functional from pseudopotentials
    when `input_dft` is unset).
    """

    ecutwfc: Annotated[
        float,
        Spec(
            (
                "xml.input.basis.ecutwfc",
                lambda ecut: ecut * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Kinetic-energy cutoff for wavefunctions in eV."""

    ecutrho: Annotated[
        float,
        Spec(
            (
                "xml.input.basis.ecutrho",
                lambda ecut: ecut * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Kinetic-energy cutoff for the charge density and potential in eV."""

    fft_grid: Annotated[
        list,
        Spec(
            (
                "xml.output.basis_set.fft_grid",
                lambda grid: [grid["@nr1"], grid["@nr2"], grid["@nr3"]],
            )
        ),
    ]
    """Charge-density FFT grid dimensions `[nr1, nr2, nr3]` (used for the density and potentials)."""

    smooth_fft_grid: Annotated[
        list,
        Spec(
            (
                "xml.output.basis_set.fft_smooth",
                lambda grid: [grid["@nr1"], grid["@nr2"], grid["@nr3"]],
            )
        ),
    ]
    """Smooth FFT grid dimensions `[nr1, nr2, nr3]` (used for wavefunctions)."""

    xc_functional: Annotated[str, Spec("xml.output.dft.functional")]
    """Name of the exchange-correlation functional (e.g. `PBESOL`)."""

    monkhorst_pack_grid: Annotated[
        list,
        Spec(
            (
                "xml.input.k_points_IBZ.monkhorst_pack",
                lambda mp: [mp["@nk1"], mp["@nk2"], mp["@nk3"]],
            )
        ),
    ]
    """Monkhorst-Pack k-point mesh `[nk1, nk2, nk3]`."""

    monkhorst_pack_offset: Annotated[
        list,
        Spec(
            (
                "xml.input.k_points_IBZ.monkhorst_pack",
                lambda mp: [mp["@k1"], mp["@k2"], mp["@k3"]],
            )
        ),
    ]
    """Monkhorst-Pack k-point shift flags `[k1, k2, k3]` (each 0 or 1; `1` shifts by half a grid step along that axis)."""

    smearing_type: Annotated[str, Spec("xml.input.bands.smearing.$")]
    """Smearing function (e.g. `mv`, `gaussian`, `fd`, `mp`)."""

    degauss: Annotated[
        float,
        Spec(
            (
                "xml.input.bands.smearing.@degauss",
                lambda d: d * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Smearing width in eV."""

    occupations: Annotated[str, Spec("xml.input.bands.occupations")]
    """Occupations scheme (e.g. `smearing`, `tetrahedra`, `fixed`)."""

    noncolin: Annotated[bool, Spec("xml.input.spin.noncolin")]
    """Whether a non-collinear magnetic calculation was performed."""

    lspinorb: Annotated[bool, Spec("xml.input.spin.spinorbit")]
    """Whether spin-orbit coupling was included."""

    noinv: Annotated[bool, Spec("xml.input.symmetry_flags.noinv")]
    """Whether inversion symmetry was disabled (`noinv=.true.`)."""

    no_t_rev: Annotated[bool, Spec("xml.input.symmetry_flags.no_t_rev")]
    """Whether time-reversal symmetry was disabled (`no_t_rev=.true.`)."""

    assume_isolated: Annotated[
        str, Spec("xml.input.boundary_conditions.assume_isolated")
    ]
    """Boundary-conditions / isolation scheme (e.g. `makov-payne`, `martyna-tuckerman`)."""


@output_mapping
class _PwMapping:
    """Typed outputs of a pw.x calculation."""

    parameters: _PwParametersMapping
    """Parameters the calculation ran with: cutoffs, grids, XC functional, k-points, spin/symmetry flags."""

    structure: Annotated[
        dict,
        Spec(
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
        ),
    ]
    """Crystal structure: cell vectors (Å), element symbols, and Cartesian positions (Å)."""

    forces: Annotated[
        list,
        Spec(
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
        ),
        Unit("eV/angstrom"),
    ]
    """Forces on atoms in eV/Å, shape [n_atoms][3]."""

    stress: Annotated[
        list,
        Spec(
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
        ),
        Unit("GPa"),
    ]
    """Stress tensor in GPa, shape [3][3]."""

    fermi_energy: Annotated[
        float,
        Spec(
            (
                "xml.output.band_structure.fermi_energy",
                lambda energy: energy * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Fermi energy in eV."""

    fermi_energy_up: Annotated[
        float,
        Spec(
            (
                "xml.output.band_structure.two_fermi_energies",
                lambda energies: energies[0] * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Fermi energy of spin-up channel in eV.

    Only available when ``tot_magnetization`` is set in ``SYSTEM``.
    """

    fermi_energy_down: Annotated[
        float,
        Spec(
            (
                "xml.output.band_structure.two_fermi_energies",
                lambda energies: energies[1] * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Fermi energy of spin-down channel in eV.

    Only available when ``tot_magnetization`` is set in ``SYSTEM``.
    """

    number_of_k_points: Annotated[int, Spec("xml.output.band_structure.nks")]
    """Number of k-points at which the Kohn-Sham states were computed."""

    k_points_weights: Annotated[
        list,
        Spec(
            (
                "xml.output.band_structure.ks_energies",
                [lambda ks: ks["k_point"]["@weight"]],
            )
        ),
    ]
    """Weights of the k-points at which the Kohn-Sham states were computed.

    Dimensionless; per QE convention the weights sum to 2 for `nspin=1` and to 1 for `nspin=2`.
    """

    k_points_cartesian: Annotated[
        list,
        Spec(
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
        ),
        Unit("1/angstrom"),
    ]
    """Cartesian coordinates of the k-points in 1/Å, shape `[n_kpoints][3]`."""

    number_of_bands: Annotated[
        int,
        Spec(
            Coalesce(
                "xml.output.band_structure.nbnd",
                "xml.output.band_structure.nbnd_up",
            )
        ),
    ]
    """Number of Kohn-Sham bands (per spin channel for spin-polarized calculations)."""

    total_energy: Annotated[
        float,
        Spec(
            (
                "xml.output.total_energy.etot",
                lambda energy: energy * CONSTANTS.hartree_to_ev,
            )
        ),
        Unit("eV"),
    ]
    """Total energy in eV."""


class PwOutput(BaseOutput[_PwMapping]):
    """Output of the Quantum ESPRESSO pw.x code."""

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
