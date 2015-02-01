"""Exception classes
"""


class ValveException(Exception):
    """Base Exception
    """
    pass


class ValveKeyError(ValveException):
    """KeyError specific to map parsing
    """
    pass


class ValveTypeError(ValveException):
    """TypeError specific to map parsing
    """
    pass
