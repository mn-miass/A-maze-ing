import sys
from typing import Any
from error_file import *
from define import *
from file_checker import *

"""list of function that should hundle different types"""
def get_value_int(line):
    try:
        key, value = line.split("=")
        value = int(value)
        return ({key: value})
    except ValueError:
        pass

def get_value_float(line):
    try:
        key, value = line.split("=")
        value = int(value)
        return ({key: value})
    except ValueError:
        pass


def get_value_str(line):
    try:
        key, value = line.split("=")
        value = int(value)
        return ({key: value})
    except ValueError:
        pass


def get_value_tuple(line):
    try:
        key, values = line.split("=")
        value1, value2 = values.split(":")
        value1 = int(value1)
        value2 = int(value2)
        return ({key: (value1, value2)})
    except ValueError:
        pass

#need to check for invalid values error for first invalid value
#need to check the data i need to read
def parsing() -> list[Any]:

    try:
        dict_values = {}
        with open(sys.argv[1]) as file:
            dict_values = check_file(file)
            for key in dict_values:

                if key == "WIDTH":
                    try:
                        if dict_values[key] == "":
                            raise InvalidWidth(NO_INPUT)
                        dict_values[key] = int(dict_values[key])
                    except ValueError:
                            raise InvalidWidth(WRONG_INPUT)

                elif key == "HEIGHT":
                    try:
                        if dict_values[key] == "":
                            raise InvalidHeight(NO_INPUT)
                        dict_values[key] = int(dict_values[key])
                    except ValueError:
                            raise InvalidHeight(WRONG_INPUT)

                elif key == "EXIT":
                    try:
                        if dict_values[key] == "":
                            raise InvalidExit(NO_INPUT)
                        x, y = dict_values[key].split(",") 
                        x = int(x)
                        y = int(y)
                        dict_values[key] = (x, y)
                    except ValueError:
                        raise InvalidExit(WRONG_INPUT)
                
                elif key == "ENTRY":
                    try:
                        if dict_values[key] == "":
                            raise InvalidEntry(NO_INPUT)
                        x, y = dict_values[key].split(",") 
                        x = int(x)
                        y = int(y)
                        dict_values[key] = (x, y)
                    except ValueError:
                        raise InvalidEntry(WRONG_INPUT)

                elif key == "OUTPUT_FILE":
                    if dict_values[key] == "":
                        raise InvalidEntry(NO_INPUT)
                        
                elif key == "PERFECT":
                    if dict_values[key] == "":
                        raise InvalidPerfect(NO_INPUT)
                    if dict_values[key].upper() not in PERFECT_VALUES:
                        raise InvalidPerfect(WRONG_INPUT)
                else:
                    raise InvalidSyntax
            print(dict_values)

    except FileNotFoundError:
        print("File not found", file=sys.stderr)

    except IndexError:
        print("No file was provided", file=sys.stderr)
    
    except (InvalidSyntax, InvalidWidth, InvalidHeight, InvalidEntry, 
            InvalidExit, InvalidOutputFile, InvalidPerfect, 
            InvalidSeed)  as e:
        print(e, file=sys.stderr)
        exit()


parsing()