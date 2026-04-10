from .line_validator import LineValidator
from .file_validator import FileValidator
from .key_value_validator import KeyValueValidator
from .log_file import LogFile
"""
parsing:
    validate the given file by checking if:
        the given name is not a directory
        the given name have the right permission
        no binary data was given
        the file really exist
            if any error happen the program will exist
            else it will read the file (if the permmision is read) and store it in data

    validate the lines:
        remove the empty lines
        remove the comments(even for the once in the middle of the line)
        remove the non vlid lines that dont contain = sign

    validat values:
        check for invalid keys
        check for invalid values 
        check for missing data

    e
    Returns:
        _type_: _description_
"""
#a small errro in missing need to be hundle even valid variable was given it still show all as missing
#logfile not working for now need to be checked
#still some error with the log file overall almost is don




#display will be in two ways

#display in terminal if one of the file is not valid except output file or the program was killed ctrl + c
#display in logfile for any other case 


#check the first condition:
#   permissions(config.txt, log_file)
#   dictionary(config.txt, log_file)
#   filenotfound(config.txt)
#   binaruy file (config.txt)
#   ctr+c check outside this


def display(invalid_value):
    for key in invalid_value:
        print(f"{key} with {invalid_value[key]} is invalid")


def display_missing(missing_value):
    for key in missing_value:
        print(f"{key} is missing")


def parsing(file_name):
    file = FileValidator(file_name)
    lines = LineValidator(file.data)
    valid_data = KeyValueValidator(lines.valid_lines)

    if not file.is_validate:
        print(file.errors[0])
        return None

    elif 'LOG_FILE' in valid_data.valid_dict:
        LogFile(valid_data.valid_dict["LOG_FILE"],
                lines.comments,
                lines.invalid_lines_no_sign,
                lines.final_report,
                valid_data.non_valid_key,
                valid_data.non_valid_value,
                valid_data.missing_keys)

    if valid_data.missing_keys and 'LOG_FILE' not in valid_data.valid_dict:
        display(valid_data.non_valid_value)
        display_missing(valid_data.missing_keys)
        return None

    return valid_data.valid_dict