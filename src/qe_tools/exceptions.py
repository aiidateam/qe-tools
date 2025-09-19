__all__ = ("ParsingError", "InputValidationError", "PathIsNotAFileError")


class ParsingError(Exception):
    """
    Generic error raised when there is a parsing error
    """


class InputValidationError(Exception):
    """
    The input data for a calculation did not validate (e.g., missing
    required input data, wrong data, ...)
    """


class PathIsNotAFileError(OSError):
    """
    The path is pointing to an object that is not a valid file.
    """
