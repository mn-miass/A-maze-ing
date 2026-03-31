import sys
from typing import Any
from error_file import *
from define import *
from file_checker import *

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
    
    except InvalidValues  as e:
        print(e, file=sys.stderr)
        exit()

    except PermissionError:
        print("Can't Read the File")
        exit()

    except IsADirectoryError:
        print("\033[91m[ERROR]Can't have citionary as output file")
        exit()

parsing()
