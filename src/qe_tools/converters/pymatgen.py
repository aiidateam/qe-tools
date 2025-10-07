from __future__ import annotations

import re
from importlib.util import find_spec

import numpy as np
from pymatgen.core.structure import Structure

from qe_tools import CONSTANTS
from qe_tools.converters.base import BaseConverter

_has_pmg = bool(find_spec("pymatgen"))
if not _has_pmg:
    raise ImportError(
        "pymatgen should be properly installed to use the pymatgen converter."
    )


class PymatgenConverter(BaseConverter):
    output_mapping = BaseConverter.output_mapping | {
        "structure": (
            Structure,
            {
                "species": (
                    "xml.output.atomic_structure.atomic_positions.atom",
                    [lambda species: re.sub(r"\d+", "", species["@name"][:2])],
                ),
                "lattice": (
                    "xml.output.atomic_structure.cell",
                    lambda cell: CONSTANTS.bohr_to_ang
                    * np.array([cell["a1"], cell["a2"], cell["a3"]]),
                ),
                "coords": (
                    "xml.output.atomic_structure.atomic_positions.atom",
                    [lambda atom: CONSTANTS.bohr_to_ang * np.array(atom["$"])],
                ),
            },
        ),
    }
