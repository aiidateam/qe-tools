# -*- coding: utf-8 -*-
"""Output of the Quantum ESPRESSO pw.x code."""

from __future__ import annotations

from pathlib import Path

from qe_tools.outputs.base import BaseOutput
from qe_tools.outputs.parsers.pw import PwStdoutParser, PwXMLParser


class PwOutput(BaseOutput):
    """Output of the Quantum ESPRESSO pw.x code."""

    def __init__(self, outputs: dict | None = None):
        super().__init__(outputs=outputs)

    @classmethod
    def from_dir(cls, directory: str | Path, filetype: str = 'both'):
        """
        From a directory, locates the standard output and XML files and
        parses them.
        """
        directory = Path(directory)

        if not directory.is_dir():
            raise ValueError(f'Path `{directory}` is not a valid directory.')

        d_out_std = {}
        d_out_xml = {}

        for file in [path for path in directory.iterdir() if path.is_file()]:
            if filetype in ['both', 'stdout']:
                with file.open('r') as handle:
                    header = ''.join(handle.readlines(5))

                    if 'Program PWSCF' in header:
                        handle.seek(0)
                        parser_std = PwStdoutParser(string=handle.read())
                        parser_std.parse()
                        d_out_std = parser_std.dict_out

            if filetype in ['both', 'xml']:
                if file.suffix == '.xml':
                    parser_xml = PwXMLParser.from_file(filename=file.as_posix())
                    parser_xml.parse()
                    d_out_xml = parser_xml.dict_out

        outputs = d_out_std | d_out_xml

        return cls(outputs=outputs)
