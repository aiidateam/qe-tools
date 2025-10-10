from __future__ import annotations

import numpy as np

from glom import T
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


def _convert_dos(energy: list, dos: list | dict):
    xy_data = orm.XyData()
    xy_data.set_x(np.array(energy), "energy", "eV")
    if isinstance(dos, dict):
        xy_data.set_y(
            [np.array(dos["dos_down"]), np.array(dos["dos_up"])],
            ["dos_spin_down", "dos_spin_down"],
            ["states/eV", "states/eV"],
        )
    else:
        xy_data.set_y(np.array(dos), "dos", "states/eV")

    return xy_data


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
        "full_dos": (
            _convert_dos,
            {
                "energy": "energy",
                "dos": (
                    T,
                    lambda full_dos: full_dos["dos"]
                    if "dos" in full_dos
                    else {
                        "dos_down": full_dos["dos_down"],
                        "dos_up": full_dos["dos_up"],
                    },
                ),
            },
        ),
    }
