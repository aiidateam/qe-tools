from __future__ import annotations

import re
from importlib.resources import files
from xml.etree import ElementTree

from xmlschema import XMLSchema

from dough.outputs import BaseOutputFileParser

from qe_tools.outputs.parsers import schemas
from qe_tools.outputs.parsers.stdout import BaseStdoutParser


class PwXMLParser(BaseOutputFileParser):
    """
    Class for parsing the XML output of pw.x.
    """

    @staticmethod
    def parse(content):
        """Parse the XML output of Quantum ESPRESSO pw.x."""

        try:
            element_root = ElementTree.fromstring(content)
        except ElementTree.ParseError:
            raise ValueError(
                "Unable to parse the XML file!\n"
                "Double-check that the file is the correct one, and is not incomplete/corrupted."
            ) from None

        str_filename = element_root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        )
        if str_filename is None:
            raise ValueError(
                "There was an error while reading the version of QE in the provided xml file."
            )

        schema_filename = str_filename.split()[1].split("/")[-1]

        # Fix issue for QE v7.0: The scheme file name was not updated to `qes_211101.xsd` in the `xsi.schemaLocation`
        # element, see https://github.com/aiidateam/aiida-quantumespresso/pull/774
        try:
            if (
                element_root.find("general_info").find("creator").get("VERSION")
                == "7.0"
            ):
                schema_filename = "qes_211101.xsd"
        except AttributeError:
            pass

        return XMLSchema(str(files(schemas) / schema_filename)).to_dict(element_root)


_HOMO_LUMO_RE = re.compile(
    r"highest occupied,\s*lowest unoccupied levels?\s*\(ev\):\s*"
    r"([\-\d.E+]+)\s+([\-\d.E+]+)"
)
_HOMO_RE = re.compile(r"highest occupied level\s*\(ev\):\s*([\-\d.E+]+)")
_TOTAL_ENERGY_RE = re.compile(r"!\s+total energy\s*=\s*([\-\d.E+]+)\s*Ry")
_ALAT_RE = re.compile(r"lattice parameter \(alat\)\s*=\s*([\-\d.E+]+)\s*a\.u\.")

# Captures the `number of k points= N` line plus the following
# `cart. coord. in units 2pi/alat` block of `k( i ) = ( x y z ), wk = w` lines.
# `[^\n]*` after the count tolerates trailing variants (`(tetrahedron method)`,
# `Marzari-Vanderbilt smearing, ...`, or nothing).
_KPOINTS_BLOCK_RE = re.compile(
    r"number of k points=\s*(?P<nks>\d+)[^\n]*\n"
    r"\s*cart\. coord\. in units 2pi/alat\s*\n"
    r"(?P<rows>(?:\s*k\(\s*\d+\s*\)\s*=\s*\(\s*[\-\d.E+]+\s+[\-\d.E+]+\s+[\-\d.E+]+\s*\),\s*wk\s*=\s*[\-\d.E+]+\s*\n)+)"
)
_KPOINT_ROW_RE = re.compile(
    r"k\(\s*\d+\s*\)\s*=\s*\(\s*([\-\d.E+]+)\s+([\-\d.E+]+)\s+([\-\d.E+]+)\s*\),"
    r"\s*wk\s*=\s*([\-\d.E+]+)"
)


class PwStdoutParser(BaseStdoutParser):
    """
    Class for parsing the standard output of pw.x.
    """

    @staticmethod
    def parse(content: str) -> dict:
        parsed_data = BaseStdoutParser.parse(content)

        match = _HOMO_LUMO_RE.search(content)
        if match:
            parsed_data["highest_occupied_level"] = float(match.group(1))
            parsed_data["lowest_unoccupied_level"] = float(match.group(2))
        else:
            match = _HOMO_RE.search(content)
            if match:
                parsed_data["highest_occupied_level"] = float(match.group(1))

        # Final SCF total energy in Ry. For relax/md runs QE prints one `!` line
        # per ionic step; the final converged value is the last one.
        energy_matches = _TOTAL_ENERGY_RE.findall(content)
        if energy_matches:
            parsed_data["total_energy"] = float(energy_matches[-1])

        # k-points: take the last block, since vc-relax reprints after relaxation.
        # The stdout values are in 2pi/alat; convert to 1/Å using `alat` (also from
        # stdout, in bohr) so downstream Specs match the XML-derived units.
        kpoint_blocks = list(_KPOINTS_BLOCK_RE.finditer(content))
        alat_match = _ALAT_RE.search(content)
        if kpoint_blocks and alat_match:
            import math

            from qe_tools import CONSTANTS

            alat_ang = float(alat_match.group(1)) * CONSTANTS.bohr_to_ang
            scale = 2 * math.pi / alat_ang
            block = kpoint_blocks[-1]
            cartesian = []
            weights = []
            for row in _KPOINT_ROW_RE.finditer(block.group("rows")):
                kx, ky, kz, wk = (float(v) for v in row.groups())
                cartesian.append([kx * scale, ky * scale, kz * scale])
                weights.append(wk)
            parsed_data["number_of_k_points"] = int(block.group("nks"))
            parsed_data["k_points_cartesian"] = cartesian
            parsed_data["k_points_weights"] = weights

        return parsed_data
