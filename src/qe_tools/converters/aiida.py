from __future__ import annotations

import numpy as np
from aiida import orm

from qe_tools.converters.base import BaseConverter


def _convert_structure_data(cell, symbols, positions):
    structure = orm.StructureData(cell=cell)

    for symbol, position in zip(symbols, positions):
        structure.append_atom(position=position, symbols=symbol)

    return structure


class AiiDAConverter(BaseConverter):
    conversion_mapping = {
        "structure": (
            _convert_structure_data,
            {
                "symbols": "atomic_species",
                "cell": ("cell", lambda cell: np.array(cell)),
                "positions": ("positions", lambda positions: np.array(positions)),
            },
        ),
    }
