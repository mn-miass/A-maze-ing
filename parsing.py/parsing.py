from line_validator import LineValidator
from file_validator import FileValidator
from key_value_validator import KeyValueValidator
from log_file import LogFile

#still some error with the log file overall almost is don
def display(invalid_value):
    for key in invalid_value:
        print(f"{key} with {invalid_value[key]} is invalid")


def display_missing(missing_value):
    for key in missing_value:
        print(f"{key} is missing")


def parsing(file_name):
    file = FileValidator(file_name)

    if not file.is_validate:
        print(file.errors[0])
        return None

    lines = LineValidator(file.data)


    valid_data = KeyValueValidator(lines.valid_lines)

    if len(valid_data.missing_keys) == 0:
        display(valid_data.non_valid_value)
        display_missing(valid_data.missing_keys)
        return None

    print(valid_data.valid_dict.keys())

    if "LOG_FILE" in list(valid_data.valid_dict.keys()):
        log = LogFile(valid_data.valid_dict["LOG_FILE"],
                    lines.comments,
                    lines.invalid_lines_no_sign,
                    lines.final_report,
                    valid_data.non_valid_key,
                    valid_data.non_valid_value,
                    valid_data.missing_keys)

    else:
        display(valid_data.non_valid_value)
        display_missing(valid_data.missing_keys)

    return valid_data.valid_dict


parsing("config.txt")