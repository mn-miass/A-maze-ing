from define import *
from style import *

"""This file is for classes that will be raised as errors"""
#can add line and column later

class   InvalidSyntax(Exception):
    def __init__(self):
        super().__init__("Invalid input was given")


class   NoInput(Exception):
    def __init__(self, msg = "No input was provided"):
        super().__init__(msg)


class   InvalidValues(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class   InvalidWidth(InvalidValues):
    pass


class   InvalidHeight(InvalidValues):
    pass


class   InvalidEntry(InvalidValues):
    pass


class   InvalidExit(InvalidValues):
    pass


class   InvalidPerfect(InvalidValues):
    pass

class   InvalidSeed(InvalidValues):
    pass
