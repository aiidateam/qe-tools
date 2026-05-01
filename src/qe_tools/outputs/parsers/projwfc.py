"""Parsers for the output of Quantum ESPRESSO projwfc.x."""

from __future__ import annotations

import re
from io import StringIO
from pathlib import Path

import numpy as np

from dough.outputs import BaseOutputFileParser


_L_FROM_LETTER = {"s": 0, "p": 1, "d": 2, "f": 3, "g": 4}

_PDOS_ATM_RE = re.compile(
    r"\.pdos_atm#(?P<atom>\d+)\((?P<element>[A-Za-z][A-Za-z0-9]*)\)"
    r"_wfc#(?P<wfc>\d+)\((?P<l>[spdfg])\)"
    r"(?:_j#(?P<j>[\d.]+))?$"
)


def _split_columns(content: str) -> tuple[list[str], np.ndarray]:
    header, _, body = content.partition("\n")
    if not header.startswith("#"):
        raise ValueError(f"Unexpected PDOS file header: {header!r}")
    columns = header.lstrip("#").split()
    array = np.loadtxt(StringIO(body), ndmin=2)
    return columns, array


class PdosAtmWfcParser(BaseOutputFileParser):
    """Parse a single ``<filpdos>.pdos_atm#N(El)_wfc#M(L)[_j#J]`` file.

    Returned dict shape:
    - `energies`: shape `(n_energies,)`
    - `ldos`: shape `(n_energies,)` (spin-unpolarised) or `(n_energies, 2)` with
      `[:, 0]` spin-up and `[:, 1]` spin-down (spin-polarised).
    - `pdos_m`: shape `(n_energies, 2*l + 1)` (spin-unpolarised) or
      `(n_energies, 2, 2*l + 1)` (spin-polarised), giving the per-magnetic-quantum-number
      projection.
    """

    @staticmethod
    def parse(content: str) -> dict:
        columns, data = _split_columns(content)
        energies = data[:, 0]
        # Number of `ldos` columns tells us spin / non-collinear shape: 1 -> nospin,
        # 2 -> collinear LSDA (ldos_up, ldos_dw).
        n_ldos = sum(1 for col in columns[1:] if col.startswith("ldos"))
        ldos = data[:, 1 : 1 + n_ldos]
        pdos_m = data[:, 1 + n_ldos :]

        if n_ldos == 1:
            return {
                "energies": energies,
                "ldos": ldos[:, 0],
                "pdos_m": pdos_m,
            }
        # Spin-polarised: pdos_m has 2*(2l+1) columns, interleaved (m1up, m1dw, ...).
        # QE writes them grouped per spin per m: convention is up_m1, dw_m1, up_m2, ...
        # We reshape to `(n_energies, 2, 2l+1)`.
        n_m = pdos_m.shape[1] // 2
        pdos_m = pdos_m.reshape(-1, n_m, 2).swapaxes(1, 2)
        return {
            "energies": energies,
            "ldos": ldos,
            "pdos_m": pdos_m,
        }


class PdosTotParser(BaseOutputFileParser):
    """Parse a ``<filpdos>.pdos_tot`` file.

    Returned dict:
    - `energies`: shape `(n_energies,)`
    - `dos_total`: total DOS (states/eV); shape `(n_energies,)` or `(n_energies, 2)` for
      spin-polarised LSDA (`[:, 0]` spin-up, `[:, 1]` spin-down).
    - `pdos_total`: sum over all atomic-orbital projections; same shape as `dos_total`.
    """

    @staticmethod
    def parse(content: str) -> dict:
        columns, data = _split_columns(content)
        energies = data[:, 0]
        rest = columns[1:]
        n_dos = sum(1 for col in rest if col.startswith("dos"))
        n_pdos = sum(1 for col in rest if col.startswith("pdos"))
        dos = data[:, 1 : 1 + n_dos]
        pdos = data[:, 1 + n_dos : 1 + n_dos + n_pdos]
        if n_dos == 1:
            dos = dos[:, 0]
        if n_pdos == 1:
            pdos = pdos[:, 0]
        return {
            "energies": energies,
            "dos_total": dos,
            "pdos_total": pdos,
        }


def parse_pdos_filename(name: str) -> dict | None:
    """Extract `(atom, element, wfc, l, j)` from a `<filpdos>.pdos_atm#...` filename.

    Returns `None` if the filename does not match the projwfc PDOS naming scheme.
    """
    match = _PDOS_ATM_RE.search(name)
    if match is None:
        return None
    info = {
        "atom": int(match.group("atom")),
        "element": match.group("element"),
        "wfc": int(match.group("wfc")),
        "l": _L_FROM_LETTER[match.group("l")],
        "l_label": match.group("l"),
    }
    if match.group("j"):
        info["j"] = float(match.group("j"))
    return info


def collect_pdos_files(
    directory: Path,
) -> tuple[list[dict], dict | None, set[Path]]:
    """Discover and parse all PDOS files in `directory`.

    Returns:
    - list of records, one per `pdos_atm#N(El)_wfc#M(L)[_j#J]` file. Each record carries
      the parsed identifiers (atom index, element, wfc index, l, optional j) and the
      parsed numerical arrays (`energies`, `ldos`, `pdos_m`). Sorted by `(atom, wfc, j)`.
    - the parsed `pdos_tot` dict (or `None` if the file is missing).
    - the set of paths consumed (so callers can skip them when looking at the rest of the
      directory, e.g. to find the projwfc.x stdout).
    """
    records: list[dict] = []
    total: dict | None = None
    consumed: set[Path] = set()
    for path in directory.iterdir():
        if not path.is_file():
            continue
        if path.name.endswith(".pdos_tot"):
            total = PdosTotParser.parse_from_file(path)
            consumed.add(path)
            continue
        info = parse_pdos_filename(path.name)
        if info is None:
            continue
        info.update(PdosAtmWfcParser.parse_from_file(path))
        records.append(info)
        consumed.add(path)
    records.sort(key=lambda r: (r["atom"], r["wfc"], r.get("j", 0.0)))
    return records, total, consumed
