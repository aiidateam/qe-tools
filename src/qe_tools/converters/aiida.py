from __future__ import annotations

import re

import numpy as np
from aiida import orm

from qe_tools import CONSTANTS
from qe_tools.converters.base import BaseConverter


def _convert_structure_data(cell, symbols, positions):
    structure = orm.StructureData(cell=cell)

    for symbol, position in zip(symbols, positions):
        structure.append_atom(position=position, symbols=symbol)

    return structure


class AiiDAConverter(BaseConverter):
    output_mapping = BaseConverter.output_mapping | {
        "structure": (
            _convert_structure_data,
            {
                "symbols": (
                    "xml.output.atomic_structure.atomic_positions.atom",
                    [lambda species: re.sub(r"\d+", "", species["@name"][:2])],
                ),
                "cell": (
                    "xml.output.atomic_structure.cell",
                    lambda cell: CONSTANTS.bohr_to_ang
                    * np.array([cell["a1"], cell["a2"], cell["a3"]]),
                ),
                "positions": (
                    "xml.output.atomic_structure.atomic_positions.atom",
                    [lambda atom: CONSTANTS.bohr_to_ang * np.array(atom["$"])],
                ),
            },
        ),
    }
