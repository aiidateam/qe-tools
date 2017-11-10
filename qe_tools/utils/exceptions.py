
class ParsingError(Exception):
    """
    Generic error raised when there is a parsing error
    """
    pass


class InputValidationError(Exception):
    """
    The input data for a calculation did not validate (e.g., missing
    required input data, wrong data, ...)
    """
    pass
