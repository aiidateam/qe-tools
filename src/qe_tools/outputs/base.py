# -*- coding: utf-8 -*-
"""Base parser for the outputs of Quantum ESPRESSO."""

import abc
import traceback


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for the parsing of output files of Quantum ESPRESSO.
    """

    def __init__(self, filename: str | list | None = None, executable: str | None = None):
        self.filename = filename or None
        self.executable = executable or None
        self.dict_out: dict = {}

    @abc.abstractmethod
    def parse_stdout(self, output_file, *args, **kwargs):
        """Parse the standard output of Quantum ESPRESSO."""
        pass

    @abc.abstractmethod
    def parse_xml(self, xml_file, *args, **kwargs):
        """Parse the XML output of Quantum ESPRESSO."""
        pass

    def parse(self):
        """
        Parse the output file of Quantum ESPRESSO pw.x.
        Uses the extension of the file to define whether an xml
        or text file should be parsed.
        In case filename is a list, loops over each file.
        """
        if isinstance(self.filename, str):
            filename = [self.filename]
        elif isinstance(self.filename, list):
            filename = self.filename
        else:
            raise TypeError(f'{self.filename} should be a string or list')

        for _i_f, fname in enumerate(filename):
            # TODO: deal with the multiple filenames in some cases
            # Should they simply be added as separate entries in self.dict_out?
            # This would work for neb.x, but I don't know for other executables.
            if fname.endswith('.xml'):
                self.parse_xml(fname)
            else:
                try:
                    self.parse_stdout(fname)
                except Exception as e:
                    raise ValueError(
                        f'An error ({type(e).__name__}) occurred when reading {fname}. Stack trace: \n {traceback.format_exc()}'
                    )

    @classmethod
    def from_dir(cls, directory: str):
        pass
