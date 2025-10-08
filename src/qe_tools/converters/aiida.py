from __future__ import annotations

import numpy as np

from qe_tools.converters.base import BaseConverter

try:
    from aiida import orm
except ImportError:
    raise ModuleNotFoundError(
        "Unable to import the 'aiida.orm' module.\n"
        "Consider (re)installing 'qe-tools` with the 'aiida' extra:\n\n"
        "  pip install qe-tools[aiida]"
    ) from None


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
