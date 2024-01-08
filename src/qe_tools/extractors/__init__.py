# -*- coding: utf-8 -*-
from pathlib import Path

from qe_tools.exceptions import PathIsNotAFile
from qe_tools.parsers import CpInputFile, PwInputFile

SUPPORTED_PARSERS = [
    'PW',
    'CP',
]


def extract(filepath: str, parser: str) -> dict:
    """Extract QE input file as a dictionary.

    Parameters
    ----------
    `filepath` : `str`
        The path to the file.
    `parser` : `str`
        The QE parser type. Supported: ['PW', 'CP']

    Returns
    -------
    `dict`
        The parsed input as a dictionary.

    Raises
    ------
    `FileNotFoundError`
        If the file does not exist.
    `PathIsNotAFile`
        If the path does not point to a file.
    `ValueError`
        If the parser type is not supported.
    """

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"'{filepath}' does not exist")

    if not path.is_file():
        raise PathIsNotAFile(f"'{filepath}' is not a valid file.")

    input_str = path.read_text(encoding='utf-8')
    parser = parser.upper()

    if parser == 'PW':
        return PwInputFile(input_str).as_dict()

    if parser == 'CP':
        return CpInputFile(input_str).as_dict()

    raise ValueError(f"Supported parsers: {SUPPORTED_PARSERS}; given: '{parser}'")
