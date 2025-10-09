from __future__ import annotations

import numpy as np

from qe_tools.converters.base import BaseConverter

try:
    from ase import Atoms
except ImportError:
    raise ModuleNotFoundError(
        "Unable to import from the 'ase' library.\n"
        "Consider (re)installing 'qe-tools` with the 'ase' extra:\n\n"
        "  pip install qe-tools[ase]"
    ) from None


class ASEConverter(BaseConverter):
    conversion_mapping = {
        "structure": (
            Atoms,
            {
                "symbols": "symbols",
                "cell": ("cell", lambda cell: np.array(cell)),
                "positions": ("positions", lambda positions: np.array(positions)),
            },
        ),
    }
