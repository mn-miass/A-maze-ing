import os
from .defines import *
from tools import test_msg, error_msg, success_msg, info_msg, warning_msg

class FileHandler():
    def __init__(self, name):
        self.name = name
        self.data_file = []
        self.validateddata = {}
        self.valid = True

    """check 3 things about the opened file: can it be opened can it be readed isn't a dictionary"""
    def FileCheck(self):
        test_msg("Opening the file")
        try:
            with open(self.name, "r") as f:
                success_msg("File opened successfully")
                info_msg("The file exist")
                info_msg("The file have the right permission(read)")
        except PermissionError:
            error_msg("Failed to open the file: can't read the file (check the permission)")
            exit()
        except FileNotFoundError:
            error_msg("Failed to open the file: the file don't exist ( creat one :) )")
            exit()
        except IsADirectoryError:
            error_msg("Failed to open the file: please enter a file not a directory")
            exit()

    """check if the file is not an empty file size == 0 but file with new lines + comments wont be catched by this"""
    def IsEmpty(self):
        test_msg("Checking the file size")
        if os.path.getsize(self.name) == 0:
            error_msg("The file is empty nothing to read")
            exit()
        else:
            success_msg("The file isn't empty")

    def GetData(self):
        test_msg("Reding the file")
        with open(self.name, "r") as file:
            self.data_file = file.readlines()
            success_msg("The data was readed")


    """if the line contain any comment it will be removed [TESTED]"""
    @staticmethod
    def CutComment(line):
        try:
            line, comment = line.split("#", 1)
            return line
        except ValueError:
            return line

    """Enter the key as striped with upper for better comparing"""
    @staticmethod
    def KeyCheck(key):
        for word in valid_data.MUST_EXIST:
            if word == key:
                return True
        for word in valid_data.BONUS:
            if word == key:
                return True
        return False

    """This parse the line seperating it by = if its valid return two striped values in a dict else empty dict"""
    @staticmethod
    def ParseKeyValue(line):
        try:
            key, value = line.split("=", 1)
            key = key.strip()
            key = key.upper()
            value = value.strip()
            return {key: value}
        except ValueError:
            return {}

    """get a dict with one element (the new created one) check it value depend on the element it returns the name of the key error if there is an error with value None if there is an error with key else the dict with valid key valid value"""
    """Im only processing the height and width entry exist positions and perfect else return the key and element"""
    def GetValue(self, element):
        key = list(element.keys())[0]
        value = list(element.values())[0]

        if key == "WIDTH" or key == "HEIGHT":
            try:
                value = int(value)
                return {key: value}
            except:
                return key

        if key == "ENTRY" or key == "EXIT":
            try:
                value1, value2 = value.split(",", 1)
                value1 = int(value1)
                value2 = int(value2)
                return {key: (value1, value2)}
            except ValueError:
                return key

        if key == "PERFECT":
            if value.upper() in valid_data.PERFECT_VALUES:
                return {key: value}
            return key
        return {key: value}


    """Check the data in the list and creat a valid dict from valid data checking only the key is valid the value is int (no impossible values yet)"""
    def CheckData(self):
        line_count = 1 #this for checking the line number
        for line in self.data_file:
            line = self.CutComment(line)
            line = line.strip()
            new_element = self.ParseKeyValue(line)
            if bool(new_element) == False:
                if line == "":
                    warning_msg(f"Invalid line: {line_count} empty line")
                else:
                    warning_msg(f"Invalid line: {line_count} {line}")
            elif self.KeyCheck(list(new_element.keys())[0]) == False:
                warning_msg(f"Invalid line: {line_count} {list(new_element.keys())[0]} not a valid input")
                #i need to skip the next if conditions from here for this line no need to heck its value if its wrong
            else :
                new_element = self.GetValue(new_element)
                if isinstance(new_element, str):
                    warning_msg(f"Invalid line: {line_count} {new_element} have invalid input")
                else:
                    #only if all tests passed it will be added key the value 
                    #not all values are tested yet
                    self.validateddata = self.validateddata | new_element
            line_count += 1


    def CountData(self):
        all_exist = True
        for key in valid_data.MUST_EXIST:
            try:
                self.validateddata[key]
            except KeyError:
                error_msg(f"Missing {key} element")
                all_exist = False
        return all_exist


    """Check if the data is really valid by checking """
    def DataIsValid(self):
        test_msg("Testing the given data")
        for data in self.validateddata:
            test_msg(f"{data}")
        if self.CountData():
            self.valid = False

        if self.CheckWidth():
            self.valid = False

        if self.CheckEntryExit():
            self.valid = False

        if self.CheckOutputfile():
            self.valid = False

        if self.CheckPerfect():
            self.valid = False


    """All the checks file return True for non valid else false"""
    """Look for width must be positive + width cant be 0 or 1"""
    def CheckWidth(self):
        try:
            value = self.validateddata["WIDTH"]
            if value == 0 or value == 1 or value < 0:
                error_msg(f"Invalide data was given to WIDTH {value}")
        except KeyError:
            self.valid = False
            pass

    """Look for height must be positive + width cant be 0 or 1"""
    def CheckHeight(self):
        try:
            value = self.validateddata["HEIGHT"]
            if value == 0 or value == 1 or value < 0:
                error_msg(f"Invalide data was given to HEIGHT {value}")
        except KeyError:
            self.valid = False
            pass

    """Look for entry and exit must be positive + they cant be on the same point or 42 blook"""
    def CheckEntryExit(self):
        try:
            value1, value2 = self.validateddata["EXIT"]
            if value1 < 0:
                error_msg(f"Invalide data was given to EXIT {value1}")
            if value2 < 0:
                error_msg(f"Invalide data was given to EXIT {value2}")
        except KeyError:
            self.valid = False
            pass

        try:
            value1, value2 = self.validateddata["ENTRY"]
            if value1 < 0:
                error_msg(f"Invalide data was given to ENTRY {value1}")
            if value2 < 0:
                error_msg(f"Invalide data was given to ENTRY {value2}")
        except KeyError:
            self.valid = False
            pass

    """check the output file cant be a dictionary check the permission and cant be one of my files"""
    def CheckOutputfile(self):
        try:
            value = self.validateddata["OUTPUT_FILE"]
            with open(self.validateddata["OUTPUT_FILE"]) as file:
                file.write("")
        except PermissionError:
            error_msg(f"Failed to open the file {self.validateddata['OUTPUT_FILE']}: can't read the file (check the permission)")
        except FileNotFoundError:
            error_msg(f"Failed to open the file {self.validateddata['OUTPUT_FILE']}: the file don't exist (creat one :)")
        except IsADirectoryError:
            error_msg(f"Failed to open the file {self.validateddata['OUTPUT_FILE']}: please enter a file not a directory")
        except KeyError:
            self.valid = False
            pass

    """check the perfect value"""
    def CheckPerfect(self):
        try: 
            value = self.validateddata["PERFECT"]
            for data in valid_data.PERFECT_VALUES:
                if data == self.validateddata["PERFECT"]:
                    return False
            raise ValueError
        except KeyError:
            error_msg(f"Invalide data was given to PERFECT {self.validateddata['PERFECT']}")
            self.valid = False

    def CheckSeed(self):
        pass

    def CheckLogFile(self):
        pass
