# -*- coding: utf-8 -*-

from ._input_base import _BaseInputFile

__all__ = ('CpInputFile',)


class CpInputFile(_BaseInputFile):
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

    :raises IOError: if ``content`` is a file and there is a problem reading
        the file.
    :raises TypeError: if ``content`` is a list containing any non-string
        element(s).
    :raises qe_tools.utils.exceptions.ParsingError: if there are issues
        parsing the content.
    """
