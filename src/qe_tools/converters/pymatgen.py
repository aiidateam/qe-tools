from __future__ import annotations

from importlib.util import find_spec

import numpy as np
from pymatgen.core.structure import Structure

from qe_tools.converters.base import BaseConverter

_has_pmg = bool(find_spec("pymatgen"))
if not _has_pmg:
    raise ImportError(
        "pymatgen should be properly installed to use the pymatgen converter."
    )


class PymatgenConverter(BaseConverter):
    conversion_mapping = {
        "structure": (
            Structure,
            {
                "species": "symbols",
                "lattice": ("cell", lambda cell: np.array(cell)),
                "coords": ("positions", lambda positions: np.array(positions)),
            },
        ),
    }
