from __future__ import annotations

import typing

from dough.converters import BaseConverter


class PymatgenConverter(BaseConverter):
    @classmethod
    def get_conversion_mapping(cls) -> dict[str, typing.Any]:
        import numpy as np

        try:
            from pymatgen.core.structure import Structure
        except ImportError:
            raise ModuleNotFoundError(
                "Unable to import from the 'pymatgen' library.\n"
                "Consider (re)installing 'qe-tools` with the 'pymatgen' extra:\n\n"
                "  pip install qe-tools[pymatgen]"
            ) from None

        return {
            "structure": (
                Structure,
                {
                    "species": "symbols",
                    "lattice": ("cell", lambda cell: np.array(cell)),
                    "coords": ("positions", lambda positions: np.array(positions)),
                },
            ),
        }
