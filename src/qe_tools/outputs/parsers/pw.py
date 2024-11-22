# -*- coding: utf-8 -*-
from __future__ import annotations

from importlib.resources import files
from xml.etree import ElementTree

from xmlschema import XMLSchema  # GB@Marnik: Could this be avoided?

from qe_tools.outputs.parsers import schemas
from qe_tools.outputs.parsers.base import BaseOutputFileParser, BaseStdoutParser


class PwXMLParser(BaseOutputFileParser):
    """
    Class for parsing the XML output of pw.x.
    """

    def __init__(self, string: str):
        super().__init__(string=string)

    def parse(self):
        """Parse the XML output of Quantum ESPRESSO pw.x."""

        xml_parsed = ElementTree.ElementTree(ElementTree.fromstring(self.string))
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


class PwStdoutParser(BaseStdoutParser):
    """
    Class for parsing the standard output of pw.x.
    """

    def __init__(self, string: str):
        super().__init__(string=string)
