from glom import glom

import numpy as np

from qe_tools import CONSTANTS


class BaseConverter:
    output_mapping = {
        "structure": (
            dict,
            {
                "atomic_species": (
                    "xml.output.atomic_species.species",
                    [lambda species: species["@name"]],
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
        "fermi_energy": (float, "xml.output.band_structure.fermi_energy"),
    }

    @classmethod
    def get_output(cls, output: str, raw_outputs: dict):
        output_converter, output_spec = cls.output_mapping[output]

        arguments = glom(raw_outputs, output_spec)

        if isinstance(arguments, dict):
            return output_converter(**arguments)
        if isinstance(arguments, list):
            return output_converter(*arguments)
        else:
            return output_converter(arguments)
