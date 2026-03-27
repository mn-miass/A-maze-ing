from define import *
from error_file import *
import sys

def key_validation(key: str) -> bool:
    if key.upper() in KEY_NAME:
        return True
    return False


def invalid_line(line):
    if line == "" or is_comment(line) == True:
        return False
    try:
        key, value = line.split("=", 1)
        key = key.strip()
        if key_validation(key) == False:
            raise ValueError
        return False
    except ValueError:
        return True


def is_comment(line):
    line = line.strip()
    if line.startswith("#"):
        return True
    return False


def check_file(file):
    try:
        dict_values = {}
        file_case = FILE_EMPTY
        lines = file.readlines()
        for line in lines :
            line = line.strip()
            if invalid_line(line) == True:
                raise InvalidSyntax
            if is_comment(line) == False and line != "":
                file_case = FILE_NOT_EMPTY
                key, value = line.split("=", 1)
                dict_values = dict_values | {key.upper(): value}
        if file_case == FILE_EMPTY:
            raise NoInput
        return dict_values
    except (NoInput, InvalidSyntax) as e:
        print(e, file=sys.stderr)
        exit()
