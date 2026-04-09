from __future__ import annotations

from dough.outputs import BaseOutputFileParser
import numpy as np
from io import StringIO
import re


class DosParser(BaseOutputFileParser):
    """
    Class for parsing the XML output of pw.x.
    """

    @staticmethod
    def parse(content: str) -> dict:
        """Parse an output `.dos` file of Quantum ESPRESSO dos.x."""

        header, _, body = content.partition("\n")

        match = re.search(r"EFermi\s=\s+([\d\.]+)\seV", header)

        if match is None:
            raise ValueError(
                f"Could not parse Fermi energy from DOS header: {header!r}"
            )

        fermi_energy = float(match.group(1))

        body_array = np.loadtxt(StringIO(body))

        parsed_data = {
            "fermi_energy": fermi_energy,
            "energy": body_array[:, 0],
            "integrated_dos": body_array[:, -1],
        }
        # Spin-polarised case
        if "dosup" in header:
            parsed_data["dos_up"] = body_array[:, 1].tolist()
            parsed_data["dos_down"] = body_array[:, 2].tolist()
        # Non-spin-polarised/non-collinear case
        else:
            parsed_data["dos"] = body_array[:, 1].tolist()

        return parsed_data
