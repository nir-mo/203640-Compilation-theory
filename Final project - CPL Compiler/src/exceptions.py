# Author: Nir Moshe.
# Date: 31-Jan-2019

# Look ma! no imports!


class CPLException(Exception):
    """Represents a general CPL compilation error."""
    def __init__(self, line, message):
        self.line = line
        self.message = message


class CPLCompoundException(CPLException):
    """Represents a collection of CPL errors."""
    def __init__(self, exceptions):
        self.exceptions = exceptions
