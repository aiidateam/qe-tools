from glom import glom
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
                    lambda cell: [
                        [coord * CONSTANTS.bohr_to_ang for coord in cell["a1"]],
                        [coord * CONSTANTS.bohr_to_ang for coord in cell["a2"]],
                        [coord * CONSTANTS.bohr_to_ang for coord in cell["a3"]],
                    ],
                ),
                "positions": (
                    "xml.output.atomic_structure.atomic_positions.atom",
                    [
                        lambda atom: [
                            CONSTANTS.bohr_to_ang * position for position in atom["$"]
                        ]
                    ],
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
