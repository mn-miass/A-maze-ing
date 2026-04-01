# I GUESS I NEED TO CONVERT THIS TO CLASS

from define import *
from error_file import *
from style import *
from tools import *

class FileChecker():
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_data = []
        self.maze_data = {}

    def process_data(self):
        msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]: {color_pallete.RESET}Processing the data"
        display_msg(msg, 0.01)
        exit_count = 0
        entry_count = 0
        output_count = 0
        height_count = 0
        width_count = 0
        perfect_count = 0
        for data in self.file_data:
                try:
                    key, value = data.split("=", 1)
                    value = value.strip()
                    key = key.strip()
                    try:
                        if key.upper() == "WIDTH":
                            width_count += 1
                            value = int(value)
                            if value == 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the WIDTH N° {width_count} have {value} 0 not allowed"
                                raise InvalidWidth(msg)
                            elif value < 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the WIDTH N° {width_count} have {value} negative not allowed"
                                raise InvalidWidth(msg)
                            self.maze_data = self.maze_data | {key.upper(): value}
                    except InvalidWidth as e:
                        display_msg(e.args[0])
                    except ValueError:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the WIDTH N° {width_count} has wrong input: {value}")

                    try:
                        if key.upper() == "HEIGHT":
                            height_count += 1
                            value = int(value)
                            if value == 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the HEIGHT N° {height_count} has wrong input: {value} 0 not allowed"
                                raise InvalidHeight(msg)
                            if value < 0:
                                f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the HEIGHT N° {height_count} has wrong input: {value} negative not allowed"
                                raise InvalidHeight(msg)
                            self.maze_data = self.maze_data | {key.upper(): value}
                    except InvalidHeight as e:
                        display_msg(e.args[0])
                    except ValueError as e:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the HEIGHT N° {height_count} has wrong input: {value}")

                    try:
                        if key.upper() == "ENTRY":
                            entry_count += 1
                            value1, value2 = value.split(",")
                            value1 = int(value1)
                            value2 = int(value2)
                            if value1 < 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the ENTRY N° {entry_count} has wrong input: {value1} negative not allowed"
                                raise InvalidEntry(msg)
                            if value2 < 0:
                                f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the ENTRY N° {entry_count} has wrong input: {value2} negative not allowed"
                                raise InvalidEntry(msg)
                    #need to check for impossible places
                            self.maze_data = self.maze_data | {key.upper(): (value1, value2)}
                    except InvalidEntry as e:
                        display_msg(e.args[0])
                    except ValueError:
                        display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: {color_pallete.RESET}the ENTRY N° {entry_count} has wrong input: {value}")

                    try:
                        if key.upper() == "EXIT":
                            exit_count += 1
                            value1, value2 = value.split(",")
                            value1 = int(value1)
                            value2 = int(value2)
                            if value1 < 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the EXIT N° {exit_count} has wrong input: {value1} negative not allowed"
                                raise InvalidExit(msg)
                            if value2 < 0:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the EXIT N° {exit_count} has wrong input: {value1} negative not allowed"
                                raise InvalidExit(msg)
                            self.maze_data = self.maze_data | {key.upper(): (value1, value2)}
                    except InvalidExit as e:
                        display_msg(e.args[0])
                    except ValueError:
                        display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: {color_pallete.RESET}the EXIT N° {entry_count} has wrong input: {value}")

                    try:
                        if key.upper() == "OUTPUT_FILE":
                            value = value.strip()
                            with open(value, "w") as file: #need to check this file not found error
                                file.write("")
                            self.maze_data = self.maze_data | {key.upper(): value}
                    except PermissionError:
                        msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the file: {value} cant be written to"
                        display_msg("INVALID DATA")
                    except IsADirectoryError:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}the OUTPUT_FILE can't be a dictionary")
                    except FileNotFoundError:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}OUTPUT_FILE not found")

                    try:
                        if key.upper() == "PERFECT":
                            value = value.strip()
                            if value.upper() not in PERFECT_VALUES:
                                msg = f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}The PERFECT value isnt valide : {value}"
                                raise InvalidPerfect(msg)
                            self.maze_data = self.maze_data | {key.upper(): value}
                    except InvalidPerfect as e:
                        display_msg(e.args[0])

                    try:
                        if key.upper() == "SEED":
                            self.maze_data = self.maze_data | {key.upper(): value}
                    except InvalidSeed:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: The seed value isnt valid")
                except ValueError:
                    pass



    def open_file(self):
        line_number = 0
        try:
            msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]: {color_pallete.RESET}Opening the file....."
            display_msg(msg, 0.01)
            with open(self.file_name) as file:
                msg = f"{color_pallete.GREEN}{style_pallete.BOLD}[SUCESS]: {color_pallete.RESET}The file{self.file_name}"
                msg += " was opened successfuly"
                display_msg(msg, 0.01)
                msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]: {color_pallete.RESET}Reading the file....."
                display_msg(msg, 0.01)
                lines = file.readlines()
                for line in lines:
                    line_number += 1
                    try :
                        self.is_invalid(line)
                    except InvalidSyntax:
                        display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: {color_pallete.RESET}Invalid input in line {line_number}")
                    if line != "\n" and self.is_comment(line) is False:
                        try:
                            line = line.split("#", 1)
                            line = line[0]
                        except ValueError:
                            pass
                        self.file_data.append(line)
                msg = f"{color_pallete.GREEN}{style_pallete.BOLD}[SUCESS]: {color_pallete.RESET}Data was readed successfully"
                display_msg(msg, 0.01)

        except FileNotFoundError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: The file don't exist")

        except PermissionError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: Can't Read the file")


        except InvalidSyntax:
            display_msg(f"{color_pallete.ORANGE}{style_pallete.BOLD}[WARNING]: Invalid line was given")

        # except

    def is_invalid(self, line):
        if line == "\n" or self.is_comment(line):
            return
        try:
            try:
                line = line.split("#", 1)
                line = line[0]
            except ValueError:
                pass
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key not in KEY_NAME:
                raise InvalidSyntax
        except ValueError:
            raise InvalidSyntax

    def process_dict(self):
        msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]: {color_pallete.RESET}Processing the given data"
        display_msg(msg)
        try:
            self.maze_data["WIDTH"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the WIDTH wasn't gived")

        try:
            self.maze_data["HEIGHT"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the HEIGHT wasn't gived")

        try:
            self.maze_data["ENTRY"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the ENTRY wasn't gived")

        try:
            self.maze_data["EXIT"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the EXIT wasn't gived")

        try:
            self.maze_data["OUTPUT_FILE"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the OUTPUT_FILE wasn't gived")

        try:
            self.maze_data["PERFECT"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the PERFECT wasn't gived")

        try:
            self.maze_data["SEED"]
        except KeyError:
            display_msg(f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: the SEED wasn't gived")

        if len(self.maze_data) == len(KEY_NAME):
            msg = f"{color_pallete.GREEN}{style_pallete.BOLD}[SUCCESS]: All the data is valid"
            display_msg(msg)
        else:
            msg = f"{color_pallete.AMEDINA}{style_pallete.BOLD}[ERROR]: MISSING DATA"
            
    @staticmethod
    def is_comment(line):
        return line.startswith("#")


file_test = FileChecker("config.txt")
file_test.open_file()
file_test.process_data()


file_test.process_dict()
# print(file_test.maze_data)