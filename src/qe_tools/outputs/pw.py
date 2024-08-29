# -*- coding: utf-8 -*-
"""Output of the Quantum ESPRESSO pw.x code."""

import os

from qe_tools.outputs.base import BaseOutput
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser


class PwOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

    def __init(self, outputs: dict | None = None):
        super().__init__(outputs=outputs, executable='pw.x')

    @classmethod
    def from_dir(cls, directory: str, filetype: str = 'both'):
        """
        From a directory, locates the standard output and XML files and
        parses them.
        """
        if not os.path.isdir(directory):
            raise ValueError(f'Directory {directory} does not exist.')

        parser_std = None
        parser_xml = None
        for file in os.listdir(directory):
            if filetype in ['both', 'stdout'] and not os.path.isdir(file):
                try:
                    with open(file, 'r') as f:
                        s = f.read()
                    if 'Program PWSCF' in s:
                        parser_std = PwStdoutParser(string=s)
                        parser_std.parse()
                except Exception:
                    raise ValueError(f'The filename {file} leads to errors when parsing.')
            if filetype in ['both', 'xml']:
                try:
                    if file.endswith('.xml'):
                        parser_xml = PwXMLParser.from_file(filename=file)
                        parser_xml.parse()
                except Exception:
                    raise ValueError(f'The filename {file} leads to errors when parsing.')

        d_out_std = {} if parser_std is None else parser_std.dict_out
        d_out_xml = {} if parser_xml is None else parser_xml.dict_out

        outputs = d_out_std | d_out_xml

        return cls(outputs=outputs)
