# -*- coding: utf-8 -*-
"""Parser for the output of the Quantum ESPRESSO pw.x code."""

from importlib.resources import files
from pathlib import Path
from xml.etree import ElementTree

import numpy
import pint
from xmlschema import XMLSchema

from qe_tools import CONSTANTS
from qe_tools.parsers import schemas


class PwParser:
    """Parser for the output of the Quantum ESPRESSO pw.x code."""

    def __init__(self, raw_data: dict = None):
        self.raw_data = raw_data or {}

    def parse_xml(self, xml_file: str | Path):
        """Parse the XML output of Quantum ESPRESSO pw.x."""

        xml_parsed = ElementTree.parse(xml_file)

        element_root = xml_parsed.getroot()
        schema_filename = (
            element_root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation').split()[1].split('/')[-1]
        )

        # Fix a bug of QE v6.8: the output XML is not consistent with schema, see
        # https://github.com/aiidateam/aiida-quantumespresso/pull/717
        try:
            if element_root.find('general_info').find('creator').get('VERSION') == '6.8':
                root = xml_parsed.getroot()
                timing_info = root.find('./timing_info')
                partial_pwscf = timing_info.find("partial[@label='PWSCF'][@calls='0']")
                try:
                    timing_info.remove(partial_pwscf)
                except (TypeError, ValueError):
                    pass
        except AttributeError:
            pass

        # Fix issue for QE v7.0: The scheme file name was not updated to `qes_211101.xsd` in the `xsi.schemaLocation`
        # element, see https://github.com/aiidateam/aiida-quantumespresso/pull/774
        try:
            if element_root.find('general_info').find('creator').get('VERSION') == '7.0':
                schema_filename = 'qes_211101.xsd'
        except AttributeError:
            pass

        self.raw_data['xml'] = XMLSchema(str(files(schemas) / schema_filename)).to_dict(xml_parsed)

    def parse_stdout(self, output_file: str | Path):
        pass

    @classmethod
    def from_dir(cls, directory: str | Path):
        pass

    def get_output_ase(self):
        """Convert the parsed data to ASE objects."""
        from ase import Atoms

        ureg = pint.UnitRegistry()

        converted_outputs = {}

        xml_dict = self.raw_data.get('xml')

        try:
            cell = (
                numpy.array([v for v in xml_dict['output']['atomic_structure']['cell'].values()])
                * CONSTANTS.bohr_to_ang
            )
            symbols = [el['@name'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']]
            positions = (
                numpy.array([el['$'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']])
                * CONSTANTS.bohr_to_ang
            )

            converted_outputs['ase_structure'] = Atoms(
                cell=cell,
                positions=positions,
                symbols=symbols,
                pbc=True,
            )
        except KeyError:
            pass

        try:
            converted_outputs['energy'] = xml_dict['output']['total_energy']['etot'] * CONSTANTS.ry_to_ev * ureg.eV
        except KeyError:
            pass

        try:
            converted_outputs['forces'] = (
                numpy.array(xml_dict['output']['forces']['$']).reshape(xml_dict['output']['forces']['@dims'])
                * 2
                * CONSTANTS.ry_to_ev
                / CONSTANTS.bohr_to_ang
                * ureg.eV
                / ureg.angstrom
            )
        except KeyError:
            pass

        return converted_outputs
