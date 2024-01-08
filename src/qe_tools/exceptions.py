# -*- coding: utf-8 -*-

__all__ = ('ParsingError', 'InputValidationError')


class ParsingError(Exception):
    """
    Generic error raised when there is a parsing error
    """


class InputValidationError(Exception):
    """
    The input data for a calculation did not validate (e.g., missing
    required input data, wrong data, ...)
    """


class PathIsNotAFile(OSError):
    """
    The path is pointing to an object that is not a valid file.
    """
