"""Parsers for the output of Quantum ESPRESSO bands.x."""

from __future__ import annotations

import re

import numpy as np

from dough.outputs import BaseOutputFileParser


_DAT_HEADER_RE = re.compile(
    r"&plot\s+nbnd\s*=\s*(?P<nbnd>\d+)\s*,\s*nks\s*=\s*(?P<nks>\d+)\s*/"
)
_RAP_HEADER_RE = re.compile(
    r"&plot_rap\s+nbnd_rap\s*=\s*(?P<nbnd>\d+)\s*,\s*nks_rap\s*=\s*(?P<nks>\d+)\s*/"
)
_HIGH_SYM_RE = re.compile(
    r"high-symmetry point:\s*"
    r"(?P<kx>[\-\d.]+)\s+(?P<ky>[\-\d.]+)\s+(?P<kz>[\-\d.]+)\s+"
    r"x coordinate\s+(?P<x>[\-\d.]+)"
)


def _parse_plot_header(
    content: str, header_re: re.Pattern, label: str
) -> tuple[int, int, str]:
    """Parse a `&plot[_rap] nbnd[_rap]=..., nks[_rap]=... /` header.

    Returns `(nbnd, nks, body)` where `body` is the remaining content after the header.
    """
    match = header_re.search(content)
    if match is None:
        raise ValueError(f"Could not parse `{label}` header from filband file.")
    return int(match.group("nbnd")), int(match.group("nks")), content[match.end() :]


class BandsDatParser(BaseOutputFileParser):
    """Parse the ``filband`` (e.g. ``MgO-bands.dat``) output of bands.x."""

    @staticmethod
    def parse(content: str) -> dict:
        nbnd, nks, body = _parse_plot_header(
            content, _DAT_HEADER_RE, "&plot nbnd=..., nks=... /"
        )

        tokens = np.fromstring(body, sep=" ")

        per_kpoint = 3 + nbnd
        expected = nks * per_kpoint
        if tokens.size != expected:
            raise ValueError(
                f"filband payload has {tokens.size} numbers; expected "
                f"{expected} for nks={nks}, nbnd={nbnd}."
            )
        block = tokens.reshape(nks, per_kpoint)

        return {
            "nbnd": nbnd,
            "nks": nks,
            "k_points": block[:, :3],
            "eigenvalues": block[:, 3:],
        }


class BandsRapParser(BaseOutputFileParser):
    """Parse the symmetry-representation ``filband.rap`` output of bands.x."""

    @staticmethod
    def parse(content: str) -> dict:
        nbnd, nks, body = _parse_plot_header(
            content, _RAP_HEADER_RE, "&plot_rap nbnd_rap=..., nks_rap=... /"
        )

        lines = body.strip().splitlines()
        if len(lines) != 2 * nks:
            raise ValueError(
                f"filband.rap has {len(lines)} body lines; expected {2 * nks} "
                f"(2 per k-point) for nks={nks}."
            )

        k_points = np.empty((nks, 3), dtype=float)
        is_high_symmetry = np.empty(nks, dtype=bool)
        representations = np.empty((nks, nbnd), dtype=int)
        for ik in range(nks):
            head = lines[2 * ik].split()
            k_points[ik] = [float(x) for x in head[:3]]
            is_high_symmetry[ik] = head[3].upper() == "T"
            representations[ik] = [int(x) for x in lines[2 * ik + 1].split()]

        return {
            "nbnd": nbnd,
            "nks": nks,
            "k_points": k_points,
            "is_high_symmetry": is_high_symmetry,
            "representations": representations,
        }


class BandsStdoutParser(BaseOutputFileParser):
    """Parse the stdout of bands.x for high-symmetry point markers."""

    @staticmethod
    def parse(content: str) -> dict:
        matches = list(_HIGH_SYM_RE.finditer(content))
        if not matches:
            return {}
        return {
            "high_symmetry_points": np.array(
                [
                    [float(m.group("kx")), float(m.group("ky")), float(m.group("kz"))]
                    for m in matches
                ]
            ),
            "high_symmetry_distances": np.array([float(m.group("x")) for m in matches]),
        }
