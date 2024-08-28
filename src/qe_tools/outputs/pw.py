# -*- coding: utf-8 -*-
"""Parser for the output of the Quantum ESPRESSO pw.x code."""

from importlib.resources import files
from xml.etree import ElementTree

from xmlschema import XMLSchema

from qe_tools.outputs import schemas
from qe_tools.outputs.base import BaseOutputFileParser


class PwParser(BaseOutputFileParser):
    """Parser for the output of the Quantum ESPRESSO pw.x code."""

    def __init__(self, filename: str | list):
        super().__init__(filename=filename, executable='pw.x')

    def parse_xml(self, xml_file: str):
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

        self.dict_out['xml'] = XMLSchema(str(files(schemas) / schema_filename)).to_dict(xml_parsed)

    def parse_stdout(self, output_file: str):
        pass

    @classmethod
    def from_dir(cls, directory: str):
        pass
