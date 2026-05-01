"""Output of the Quantum ESPRESSO projwfc.x code."""

import typing
from pathlib import Path
from typing import Annotated, TextIO

from glom import Spec

from dough.outputs import BaseOutput, output_mapping

from .parsers.projwfc import (
    PdosAtmWfcParser,
    PdosTotParser,
    collect_pdos_files,
    parse_pdos_filename,
)
from .parsers.stdout import BaseStdoutParser


@output_mapping
class _ProjwfcMapping:
    """Typed outputs of a projwfc.x calculation."""

    pdos: Annotated[list, Spec("pdos_records")]
    """Per-(atom, wavefunction) projected DOS records.

    A flat list of dicts; one entry per `<filpdos>.pdos_atm#N(El)_wfc#M(L)[_j#J]` file.
    Each record has the keys:

    - `atom` (int): 1-based atom index in the unit cell
    - `element` (str): element symbol (e.g. `"Mg"`, `"O"`)
    - `wfc` (int): 1-based wavefunction (radial-channel) index for this atom
    - `l` (int): orbital angular momentum quantum number (`0=s`, `1=p`, `2=d`, `3=f`)
    - `l_label` (str): single-letter label for `l` (`"s"`, `"p"`, ...)
    - `j` (float, optional): total angular momentum, only present for spin-orbit runs
    - `energies`: numpy array of shape `(n_energies,)` in eV
    - `ldos`: per-l projected DOS (states/eV). Shape `(n_energies,)` for
      spin-unpolarised runs, `(n_energies, 2)` for spin-polarised LSDA with
      `[:, 0]` spin-up and `[:, 1]` spin-down.
    - `pdos_m`: per-magnetic-quantum-number projection (states/eV). Shape
      `(n_energies, 2*l + 1)` for spin-unpolarised runs, `(n_energies, 2, 2*l + 1)`
      for spin-polarised LSDA with axis 1 the spin channel and axis 2 the
      magnetic quantum number `m = -l, ..., +l` in QE order.

    Filter the list with a comprehension to get the projection you want, e.g.
    `[r for r in pdos if r["element"] == "Mg" and r["l_label"] == "p"]`.
    """

    pdos_total: Annotated[dict, Spec("pdos_total")]
    """Total DOS and total projected DOS, parsed from `<filpdos>.pdos_tot`.

    Dict with keys:

    - `energies`: numpy array of shape `(n_energies,)` in eV
    - `dos_total`: total DOS (states/eV); shape `(n_energies,)` or `(n_energies, 2)` for
      spin-polarised LSDA (`[:, 0]` spin-up, `[:, 1]` spin-down).
    - `pdos_total`: sum of all atomic-orbital projections; same shape as `dos_total`.
    """


class ProjwfcOutput(BaseOutput[_ProjwfcMapping]):
    """Output of the Quantum ESPRESSO projwfc.x code."""

    converters: typing.ClassVar[dict] = {}

    @classmethod
    def from_dir(cls, directory: str | Path):
        """Locate and parse all `<filpdos>.pdos_*` files plus `projwfc.x` stdout in `directory`."""
        directory = Path(directory)

        if not directory.is_dir():
            raise ValueError(f"Path `{directory}` is not a valid directory.")

        records, total, consumed = collect_pdos_files(directory)

        stdout_file = None
        for file in directory.iterdir():
            if not file.is_file() or file in consumed:
                continue
            with file.open("r") as handle:
                header = "".join(handle.readlines(5))
            if "Program PROJWFC" in header:
                stdout_file = file
                break

        raw_outputs: dict = {"pdos_records": records, "pdos_total": total}
        if stdout_file is not None:
            raw_outputs["stdout"] = BaseStdoutParser.parse_from_file(stdout_file)

        return cls(raw_outputs=raw_outputs)

    @classmethod
    def from_files(
        cls,
        *,
        pdos_files: typing.Iterable[str | Path] = (),
        pdos_tot: None | str | Path | TextIO = None,
        stdout: None | str | Path | TextIO = None,
    ):
        """Parse the outputs from explicit file lists.

        - `pdos_files`: iterable of `<filpdos>.pdos_atm#N(El)_wfc#M(L)[_j#J]` paths
        - `pdos_tot`: `<filpdos>.pdos_tot` path
        - `stdout`: projwfc.x standard output
        """
        records: list[dict] = []
        for path in pdos_files:
            path = Path(path)
            info = parse_pdos_filename(path.name)
            if info is None:
                raise ValueError(
                    f"`{path.name}` does not match the projwfc PDOS naming scheme."
                )
            info.update(PdosAtmWfcParser.parse_from_file(path))
            records.append(info)

        raw_outputs: dict = {
            "pdos_records": records,
            "pdos_total": PdosTotParser.parse_from_file(pdos_tot)
            if pdos_tot is not None
            else None,
        }
        if stdout is not None:
            raw_outputs["stdout"] = BaseStdoutParser.parse_from_file(stdout)
        return cls(raw_outputs=raw_outputs)
