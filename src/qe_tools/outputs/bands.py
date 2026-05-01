"""Output of the Quantum ESPRESSO bands.x code."""

import typing
from pathlib import Path
from typing import Annotated, TextIO

import numpy as np
from glom import Spec

from dough import Unit
from dough.outputs import BaseOutput, output_mapping

from .parsers.bands import (
    BandsDatParser,
    BandsRapParser,
    BandsStdoutParser,
)


@output_mapping
class _BandsMapping:
    """Typed outputs of a bands.x calculation."""

    number_of_kpoints: Annotated[int, Spec("dat.nks")]
    """Number of k-points along the band-structure path."""

    number_of_bands: Annotated[int, Spec("dat.nbnd")]
    """Number of bands written by bands.x."""

    k_points: Annotated[np.ndarray, Spec("dat.k_points")]
    """Crystal-momentum coordinates of each k-point on the path.

    Numpy array of shape `(n_kpoints, 3)`; coordinates are in the same units that the
    pw.x input used for `K_POINTS` (typically `2π/alat` for `tpiba_b`, or crystal
    coordinates for `crystal_b`). bands.x does not transform them.
    """

    eigenvalues: Annotated[np.ndarray, Spec("dat.eigenvalues"), Unit("eV")]
    """Kohn-Sham eigenvalues along the band path, in eV.

    Numpy array of shape `(n_kpoints, n_bands)`:

    - axis 0 (`n_kpoints`): k-points in the order given by `k_points`
    - axis 1 (`n_bands`): band index, ascending (energy-sorted at each k-point)

    For spin-polarised calculations, bands.x writes one filband per spin channel; this
    array therefore covers a single spin channel.
    """

    high_symmetry_points: Annotated[np.ndarray, Spec("stdout.high_symmetry_points")]
    """Crystal-momentum coordinates of the high-symmetry points along the path.

    Numpy array of shape `(n_high_sym, 3)`. Reported in the same coordinate system as
    `k_points`. Parsed from the bands.x stdout.
    """

    high_symmetry_distances: Annotated[
        np.ndarray, Spec("stdout.high_symmetry_distances")
    ]
    """Cumulative path-length at each high-symmetry point.

    Numpy array of shape `(n_high_sym,)`. Units match those bands.x uses internally
    (typically `2π/alat`). Suitable for placing tick labels on the x-axis of a
    band-structure plot.
    """

    representations: Annotated[np.ndarray, Spec("rap.representations")]
    """Symmetry-representation index per (k-point, band).

    Numpy array of shape `(n_kpoints, n_bands)` of integers. Only present when bands.x
    was run with `lsym=.true.` and produced a `filband.rap` file.
    """

    is_high_symmetry: Annotated[np.ndarray, Spec("rap.is_high_symmetry")]
    """Boolean array of shape `(n_kpoints,)` flagging high-symmetry k-points.

    Only present when a `filband.rap` file is available.
    """


class BandsOutput(BaseOutput[_BandsMapping]):
    """Output of the Quantum ESPRESSO bands.x code."""

    converters: typing.ClassVar[dict] = {}

    @classmethod
    def from_dir(cls, directory: str | Path):
        """Locate filband (`*.dat`, `*.dat.rap`) and bands.x stdout in `directory`."""
        directory = Path(directory)

        if not directory.is_dir():
            raise ValueError(f"Path `{directory}` is not a valid directory.")

        rap_file = next(directory.glob("*.dat.rap"), None)

        dat_file = None
        for candidate in directory.glob("*.dat"):
            if candidate.name.endswith(".dat.rap"):
                continue
            with candidate.open("r") as handle:
                if "&plot" in handle.readline():
                    dat_file = candidate
                    break

        stdout_file = None
        for file in directory.iterdir():
            if not file.is_file():
                continue
            with file.open("r") as handle:
                header = "".join(handle.readlines(5))
            if "Program BANDS" in header:
                stdout_file = file
                break

        return cls.from_files(dat=dat_file, rap=rap_file, stdout=stdout_file)

    @classmethod
    def from_files(
        cls,
        *,
        dat: None | str | Path | TextIO = None,
        rap: None | str | Path | TextIO = None,
        stdout: None | str | Path | TextIO = None,
    ):
        """Parse the outputs directly from the provided files."""
        raw_outputs: dict = {}

        if dat is not None:
            raw_outputs["dat"] = BandsDatParser.parse_from_file(dat)
        if rap is not None:
            raw_outputs["rap"] = BandsRapParser.parse_from_file(rap)
        if stdout is not None:
            raw_outputs["stdout"] = BandsStdoutParser.parse_from_file(stdout)

        return cls(raw_outputs=raw_outputs)
