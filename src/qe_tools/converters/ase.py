from __future__ import annotations

import typing

from dough.converters import BaseConverter


class ASEConverter(BaseConverter):
    @classmethod
    def get_conversion_mapping(cls) -> dict[str, typing.Any]:
        import numpy as np

        try:
            from ase import Atoms
        except ImportError:
            raise ModuleNotFoundError(
                "Unable to import from the 'ase' library.\n"
                "Consider (re)installing 'qe-tools` with the 'ase' extra:\n\n"
                "  pip install qe-tools[ase]"
            ) from None

        return {
            "structure": (
                Atoms,
                {
                    "symbols": "symbols",
                    "cell": ("cell", lambda cell: np.array(cell)),
                    "positions": ("positions", lambda positions: np.array(positions)),
                },
            ),
        }
