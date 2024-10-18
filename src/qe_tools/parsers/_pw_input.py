# -*- coding: utf-8 -*-
"""
Tools for parsing QE PW input files
"""

import re

from ..exceptions import ParsingError
from ._input_base import RE_FLAGS, _BaseInputFile

__all__ = ('PwInputFile',)


class PwInputFile(_BaseInputFile):
    """
    Class used for parsing Quantum Espresso pw.x input files and using the info.

    Members:

    * ``namelists``:
        A nested dictionary of the namelists and their key-value
        pairs. The namelists will always be upper-case keys, while the parameter
        keys will always be lower-case.

        For example::

            {"CONTROL": {"calculation": "bands",
                         "prefix": "al",
                         "pseudo_dir": "./pseudo",
                         "outdir": "./out"},
             "ELECTRONS": {"diagonalization": "cg"},
             "SYSTEM": {"nbnd": 8,
                        "ecutwfc": 15.0,
                        "celldm(1)": 7.5,
                        "ibrav": 2,
                        "nat": 1,
                        "ntyp": 1}
            }

    * ``atomic_positions``:
        A dictionary with

            * units: the units of the positions (always lower-case) or None
            * names: list of the atom names (e.g. ``'Si'``, ``'Si0'``,
              ``'Si_0'``)
            * positions: list of the [x, y, z] positions
            * fixed_coords: list of [x, y, z] (bools) of the force modifications
              (**Note:** True <--> Fixed, as defined in the
              ``BasePwCpInputGenerator._if_pos`` method)

        For example::

            {'units': 'bohr',
             'names': ['C', 'O'],
             'positions': [[0.0, 0.0, 0.0],
                           [0.0, 0.0, 2.5]]
             'fixed_coords': [[False, False, False],
                              [True, True, True]]}

    * ``cell_parameters``:
        A dictionary (if CELL_PARAMETERS is present; else: None) with

            * units: the units of the lattice vectors (always lower-case) or
              None
            * cell: 3x3 list with lattice vectors as rows

        For example::

            {'units': 'angstrom',
             'cell': [[16.9, 0.0, 0.0],
                      [-2.6, 8.0, 0.0],
                      [-2.6, -3.5, 7.2]]}

    * ``k_points``:
        A dictionary containing

            * type: the type of kpoints (always lower-case)
            * points:
              - if type != 'automatic': an Nx3 list of the kpoints
                (will not be present if type = 'gamma')
              - if type == 'automatic': a 1x3 list of the number of
                equally-spaced points in each direction of the Brillouin zone,
                as in Monkhorst-Pack grids
            * weights: a 1xN list of the kpoint weights (will not be present if
              type = 'gamma' or type = 'automatic')
            * offset: a 1x3 list of the grid offsets in each direction of the
              Brillouin zone (only present if type = 'automatic')
              (**Note:** The offset value for each direction will be *one of*
              ``0.0`` [no offset] *or* ``0.5`` [offset by half a grid step].
              This differs from the Quantum Espresso convention, where an offset
              value of ``1`` corresponds to a half-grid-step offset, but adheres
              to the current AiiDA convention.


        Examples::

            {'type': 'crystal',
             'points': [[0.125,  0.125,  0.0],
                        [0.125,  0.375,  0.0],
                        [0.375,  0.375,  0.0]],
             'weights': [1.0, 2.0, 1.0]}

            {'type': 'automatic',
             'points': [8, 8, 8],
             'offset': [0.0, 0.5, 0.0]}

            {'type': 'gamma'}

    * ``atomic_species``:
        A dictionary with

            * names: list of the atom names (e.g. 'Si', 'Si0', 'Si_0') (case
              as-is)
            * masses: list of the masses of the atoms in 'names'
            * pseudo_file_names: list of the pseudopotential file names for the
              atoms in 'names' (case as-is)

        Example::

            {'names': ['Li', 'O', 'Al', 'Si'],
             'masses': [6.941,  15.9994, 26.98154, 28.0855],
             'pseudo_file_names': ['Li.pbe-sl-rrkjus_psl.1.0.0.UPF',
                                   'O.pbe-nl-rrkjus_psl.1.0.0.UPF',
                                   'Al.pbe-nl-rrkjus_psl.1.0.0.UPF',
                                   'Si3 28.0855 Si.pbe-nl-rrkjus_psl.1.0.0.UPF']

    """

    def __init__(self, content, *, qe_version=None, validate_species_names=True):
        """
        Parse inputs's namelist and cards to create attributes of the info.

        :param content:  A single string containing the content file's text.
        :type content: str

        :param qe_version: A string defining which version of QuantumESPRESSO
            the input file is used for. This is used in cases where different
            QE versions handle the input differently.
            If no version is specified, it will default to the latest
            implemented version.
            The string must comply with the PEP440 versioning scheme.
            Valid version strings are e.g. '6.5', '6.4.1', '6.4rc2'.
        :type qe_version: Optional[str]

        :param validate_species_names: A boolean flag (default: True) to enable
            the consistency check between atom names and species names inferred
            from the pseudopotential file name.
        :type validate_species_names: bool

        :raises IOError: if ``content`` is a file and there is a problem reading
            the file.
        :raises TypeError: if ``content`` is a list containing any non-string
            element(s).
        :raises qe_tools.utils.exceptions.ParsingError: if there are issues
            parsing the content.
        """

        super().__init__(
            content,
            qe_version=qe_version,
            validate_species_names=validate_species_names,
        )

        # Parse the K_POINTS card.
        self.k_points = parse_k_points(self._input_txt)

    def as_dict(self) -> dict:
        """Return parsed data as dictionary."""
        dictionary = super().as_dict()
        dictionary.update(
            {
                'k-points': self.k_points,
            }
        )
        return dictionary


def parse_k_points(txt):
    """
    Return a dictionary containing info from the K_POINTS card block in txt.

    .. note:: If the type of kpoints (where type = x in the card header,
           "K_POINTS x") is not present, type will be returned as 'tpiba', the
           QE default.

    :param txt: A single string containing the QE input text to be parsed.

    :returns:
        A dictionary containing

            * type: the type of kpoints (always lower-case)
            * points:
              - if type != 'automatic': an Nx3 list of the kpoints
                (will not be present if type = 'gamma')
              - if type == 'automatic': a 1x3 list of the number of
                equally-spaced points in each direction of the Brillouin zone,
                as in Monkhorst-Pack grids
            * weights: a 1xN list of the kpoint weights (will not be present if
              type = 'gamma' or type = 'automatic')
            * offset: a 1x3 list of the grid offsets in each direction of the
              Brillouin zone (only present if type = 'automatic')
              (**Note:** The offset value for each direction will be *one of*
              ``0.0`` [no offset] *or* ``0.5`` [offset by half a grid step].
              This differs from the Quantum Espresso convention, where an offset
              value of ``1`` corresponds to a half-grid-step offset, but adheres
              to the current AiiDA convention.


        Examples::

            {'type': 'crystal',
             'points': [[0.125,  0.125,  0.0],
                        [0.125,  0.375,  0.0],
                        [0.375,  0.375,  0.0]],
             'weights': [1.0, 2.0, 1.0]}

            {'type': 'automatic',
             'points': [8, 8, 8],
             'offset': [0.0, 0.5, 0.0]}

            {'type': 'gamma'}

    :raises qe_tools.utils.exceptions.ParsingError: if there are issues
        parsing the input.
    """
    # Define re for the special-type card block.
    k_points_special_block_re = re.compile(
        r"""
        ^ [ \t]* K_POINTS [ \t]*
            [{(]? [ \t]* (?P<type>\S+?)? [ \t]* [)}]? [ \t]* $\n
        ^ [ \t]* \S+ [ \t]* $\n  # nks
        (?P<block>
         (?:
          ^ [ \t]* \S+ [ \t]+ \S+ [ \t]+ \S+ [ \t]+ \S+ [ \t]* $\n?
         )+
        )
        """,
        RE_FLAGS,
    )
    # Define re for the info contained in the special-type block.
    k_points_special_re = re.compile(
        r"""
    ^ [ \t]* (\S+) [ \t]+ (\S+) [ \t]+ (\S+) [ \t]+ (\S+) [ \t]* $\n?
    """,
        RE_FLAGS,
    )
    # Define re for the automatic-type card block and its line of info.
    k_points_automatic_block_re = re.compile(
        r"""
        ^ [ \t]* K_POINTS [ \t]* [{(]? [ \t]* automatic [ \t]* [)}]? [ \t]* $\n
        ^ [ \t]* (\S+) [ \t]+ (\S+) [ \t]+ (\S+) [ \t]+ (\S+) [ \t]+ (\S+)
            [ \t]+ (\S+) [ \t]* $\n?
        """,
        RE_FLAGS,
    )
    # Define re for the gamma-type card block. (There is no block info.)
    k_points_gamma_block_re = re.compile(
        r"""
        ^ [ \t]* K_POINTS [ \t]* [{(]? [ \t]* gamma [ \t]* [)}]? [ \t]* $\n
        """,
        RE_FLAGS,
    )
    # Try finding the card block using all three types.
    info_dict = {}
    match = k_points_special_block_re.search(txt)
    if match:
        if match.group('type') is not None:
            info_dict['type'] = match.group('type').lower()
        else:
            info_dict['type'] = 'tpiba'
        blockstr = match.group('block')
        points = []
        weights = []
        for match in k_points_special_re.finditer(blockstr):
            points.append(list(map(float, match.group(1, 2, 3))))
            weights.append(float(match.group(4)))
        info_dict['points'] = points
        info_dict['weights'] = weights
    else:
        match = k_points_automatic_block_re.search(txt)
        if match:
            info_dict['type'] = 'automatic'
            info_dict['points'] = list(map(int, match.group(1, 2, 3)))
            info_dict['offset'] = [0.0 if x == 0 else 0.5 for x in map(int, match.group(4, 5, 6))]
        else:
            match = k_points_gamma_block_re.search(txt)
            if match:
                info_dict['type'] = 'gamma'
            else:
                raise ParsingError('K_POINTS card not found in\n' + txt)
    return info_dict
