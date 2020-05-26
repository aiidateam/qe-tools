# -*- coding: utf-8 -*-

from .qeinputparser import (QeInputFile, parse_namelists,
                            parse_atomic_positions, parse_atomic_species,
                            parse_cell_parameters)


class CpInputFile(QeInputFile):
    def __init__(self, pwinput, *, qe_version=None):
        """
        Parse inputs's namelist and cards to create attributes of the info.

        :param pwinput:  A single string containing the pwinput file's text.
        :type pwinput: str

        :param qe_version: A string defining which version of QuantumESPRESSO
            the input file is used for. This is used in cases where different
            QE versions handle the input differently.
            If no version is specified, it will default to the latest
            implemented version.
            The string must comply with the PEP440 versioning scheme.
            Valid version strings are e.g. '6.5', '6.4.1', '6.4rc2'.
        :type qe_version: Optional[str]

        :raises IOError: if ``pwinput`` is a file and there is a problem reading
            the file.
        :raises TypeError: if ``pwinput`` is a list containing any non-string
            element(s).
        :raises qe_tools.utils.exceptions.ParsingError: if there are issues
            parsing the pwinput.
        """

        super().__init__(pwinput, qe_version=qe_version)

        # Parse the namelists.
        self.namelists = parse_namelists(self.input_txt)
        # Parse the ATOMIC_POSITIONS card.
        self.atomic_positions = parse_atomic_positions(self.input_txt)
        # Parse the CELL_PARAMETERS card.
        self.cell_parameters = parse_cell_parameters(self.input_txt)
        # Parse the ATOMIC_SPECIES card.
        self.atomic_species = parse_atomic_species(self.input_txt)
