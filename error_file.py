from define import *


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
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the WIDTH wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the WIDTH has wrong input")
        super().__init__(msg)


class   InvalidHeight(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the HEIGHT wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the HEIGHT has wrong input")
        super().__init__(msg)


class   InvalidEntry(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the ENTRY wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the ENTRY has wrong input")
        super().__init__(msg)


class   InvalidExit(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the EXIT wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the EXIT has wrong input")
        super().__init__(msg)


class   InvalidOutputFile(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the OUTPUTFILE wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the OUTPUTFILE has wrong input")
        super().__init__(msg)


class   InvalidPerfect(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the PERFECT wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the PERFECT has wrong input")
        super().__init__(msg)


class   InvalidSeed(InvalidValues):
    def __init__(self, flag):
        if flag == NO_INPUT:
            msg = ("[ALERT]: the SEED wasn't gived")
        elif flag == WRONG_INPUT:
            msg = ("[ERROR]: the SEED has wrong input")
        super().__init__(msg)