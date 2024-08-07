# -*- coding: utf-8 -*-
"""Parser for the output of the Quantum ESPRESSO pw.x code."""

from importlib.resources import files
from pathlib import Path
from xml.etree import ElementTree

import numpy as np
import pint
from xmlschema import XMLSchema

from qe_tools import CONSTANTS, ELEMENTS
from qe_tools.outputs import schemas


class PwParser:
    """Parser for the output of the Quantum ESPRESSO pw.x code."""

    def __init__(self, raw_data: dict | None = None):
        self.raw_data = raw_data or {}

    def parse_xml(self, xml_file: str | Path):
        """Parse the XML output of Quantum ESPRESSO pw.x."""

        xml_parsed = ElementTree.parse(xml_file)

        element_root = xml_parsed.getroot()
        str_filename = element_root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        if str_filename is None:
            raise ValueError('There was an error while reading the version of QE in the provided xml file.')
        else:
            schema_filename = str_filename.split()[1].split('/')[-1]

        # Fix a bug of QE v6.8: the output XML is not consistent with schema, see
        # https://github.com/aiidateam/aiida-quantumespresso/pull/717
        try:
            if element_root.find('general_info').find('creator').get('VERSION') == '6.8':  # type: ignore
                root = xml_parsed.getroot()
                timing_info = root.find('./timing_info')
                partial_pwscf = timing_info.find("partial[@label='PWSCF'][@calls='0']")  # type: ignore
                try:
                    timing_info.remove(partial_pwscf)  # type: ignore
                except (TypeError, ValueError):
                    pass
        except AttributeError:
            pass

        # Fix issue for QE v7.0: The scheme file name was not updated to `qes_211101.xsd` in the `xsi.schemaLocation`
        # element, see https://github.com/aiidateam/aiida-quantumespresso/pull/774
        try:
            if element_root.find('general_info').find('creator').get('VERSION') == '7.0':  # type: ignore
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
                np.array([v for v in xml_dict['output']['atomic_structure']['cell'].values()]) * CONSTANTS.bohr_to_ang  # type: ignore
            )
            symbols = [el['@name'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']]  # type: ignore
            # This is to handle the case where symbols are not only
            # atom symbols (e.g., Ni1 and Ni2 in the case of an AFM computation).
            symbols_new = []
            for s in symbols:
                s_low = s.lower()
                s_elem = ''
                for e in ELEMENTS:
                    e_low = e.lower()
                    if e_low in s_low and len(e_low) > len(s_elem):
                        s_elem = e
                if s_elem == '':
                    s_elem = s
                symbols_new.append(s_elem)
            symbols = symbols_new

            positions = (
                np.array([el['$'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']])  # type: ignore
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
            converted_outputs['energy'] = xml_dict['output']['total_energy']['etot'] * CONSTANTS.ry_to_ev * ureg.eV  # type: ignore
        except KeyError:
            pass

        try:
            converted_outputs['forces'] = (
                np.array(xml_dict['output']['forces']['$']).reshape(xml_dict['output']['forces']['@dims'])  # type: ignore
                * 2
                * CONSTANTS.ry_to_ev
                / CONSTANTS.bohr_to_ang
                * ureg.eV
                / ureg.angstrom
            )
        except KeyError:
            pass

        return converted_outputs
