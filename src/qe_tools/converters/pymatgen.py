from __future__ import annotations

import numpy as np

from qe_tools.converters.base import BaseConverter

try:
    from pymatgen.core.structure import Structure
except ImportError:
    raise ModuleNotFoundError(
        "Unable to import from the 'pymatgen' library.\n"
        "Consider (re)installing 'qe-tools` with the 'pymatgen' extra:\n\n"
        "  pip install qe-tools[pymatgen]"
    ) from None


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
