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
        msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]Processing the data"
        display_msg(msg, 0.01)

        for data in self.file_data:
            key, value = data.split("=")
            try:
                if key.upper() == "WIDTH":
                    value = int(value)
                    if value == 0:
                        raise InvalidWidth(ZERO_VALUE)
                    elif value < 0:
                        raise InvalidWidth(NEGATIVE_VALUE)
                    self.maze_data = self.maze_data | {key: value}
            except InvalidWidth as e:
                print(e)
            except ValueError:
                print("INVALID VALUE")

            try:
                if key.upper() == "HEIGHT":
                    value = int(value)
                    if value == 0:
                        raise InvalidHeight(ZERO_VALUE)
                    if value < 0:
                        raise InvalidHeight(NEGATIVE_VALUE)
                    self.maze_data = self.maze_data | {key: value}
            except InvalidHeight as e:
                print(e)
            except ValueError as e:
                print("INVALID VALUE")

            try:
                if key.upper() == "ENTRY":
                    value1, value2 = value.split(",")
                    value1 = int(value1)
                    value2 = int(value2)
                    if value1 < 0:
                        raise InvalidEntry(NEGATIVE_VALUE, value1)
                    if value2 < 0:
                        raise InvalidEntry(NEGATIVE_VALUE, value2)
            #need to check for impossible places
                    self.maze_data = self.maze_data | {key: (value1, value2)}
            except InvalidEntry as e:
                print(e)
            except ValueError:
                print("INVALID DATA")

            try:
               if key.upper() == "EXIT":
                    value1, value2 = value.split(",")
                    value1 = int(value1)
                    value2 = int(value2)
                    if value1 < 0:
                        raise InvalidExit(NEGATIVE_VALUE, value1)
                    if value2 < 0:
                        raise InvalidExit(NEGATIVE_VALUE, value2)
                    self.maze_data = self.maze_data | {key: (value1, value2)}
            except InvalidExit as e:
                print(e)
            except ValueError:
                print("INVALID DATA")

            try:
               if key.upper() == "OUTPUT_FILE":
                    with open("OUTPUT_FILE") as file:
                        file.readline()
                    self.maze_data = self.maze_data | {key: value}
            except PermissionError:
                print("INVALID DATA")
            except FileNotFoundError:
                print("INVALID DATA")

            try:
                if key.upper() == "PERFECT":
                    if value not in PERFECT_VALUES:
                        raise InvalidPerfect(WRONG_INPUT)
                    self.maze_data = self.maze_data | {key: value}
            except:
                pass

            try:
                if key.upper() == "SEED":
                    self.maze_data = self.maze_data | {key: value}
            except:
                print("INVALID DATA")

    def open_file(self):
        try:
            msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]Opening the file....."
            display_msg(msg, 0.01)
            with open(self.file_name) as file:
                msg = f"{color_pallete.GREEN}{style_pallete.BOLD}[SUCESS]The file{self.file_name}"
                msg += " was opened successfuly"
                display_msg(msg, 0.01)
                msg = f"{color_pallete.MAHDI}{style_pallete.BOLD}[INFO]Reading the file....."
                display_msg(msg, 0.01)
                lines = file.readlines()
                for line in lines:
                    self.is_invalid(line)
                    if line != "\n" and self.is_comment(line) is False:
                        self.file_data.append(line)
                msg = f"{color_pallete.GREEN}{style_pallete.BOLD}[SUCESS]Data was readed successfully"
                display_msg(msg, 0.01)

        except FileNotFoundError:
            pass 

        except PermissionError:
            pass

        except InvalidSyntax:
            pass

        # except 
    def is_invalid(self, line):
        if line == "\n" or self.is_comment(line):
            return
        try:
            key, value = line.split("=")
            key = key.strip()
            value = value.strip()
            if key not in KEY_NAME:
                raise InvalidSyntax
        except ValueError:
            raise InvalidSyntax

    @staticmethod
    def is_comment(line):
        return line.startswith("#")


file_test = FileChecker("config.txt")
file_test.open_file()
file_test.process_data()
print(file_test.maze_data)
