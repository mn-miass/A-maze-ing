from typing import Any
from .file_validator import FileValidator


class KeyValueValidator():
    """
    Validates keys and values parsed from a config file.

    Separates valid entries from invalid ones, checks value formats,
    and ensures all mandatory keys are present.

    Attributes:
        valid_lines (list[str]): Raw 'KEY=VALUE' lines to validate.
        valid_dict (dict[str, Any]): Successfully validated key-value pairs.
        non_valid_key (dict[str, str]): Entries with unrecognized keys.
        non_valid_value (dict[str, Any]): Entries with invalid values.
        missing_keys (list[str]): Mandatory keys absent from valid_dict.
        is_validated (bool): False if any mandatory key is missing.
    """

    VALID_KEYS: list[str] = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT", "SEED", "LOG_FILE", "MSG"
    ]

    MANDATORY_KEYS: list[str] = [
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT"
    ]

    def __init__(self, valid_lines: list[str]) -> None:
        self.valid_lines: list[str] = valid_lines
        self.valid_dict: dict[str, Any] = {}
        self.non_valid_key: dict[str, str] = {}
        self.non_valid_value: dict[str, Any] = {}
        self.missing_keys: list[str] = []
        self.is_validated: bool = True
        self.errors: dict[str, str] = {}
        self._validate()

    def _validate(self) -> None:
        """Runs all validation steps in order."""
        self._check_key()
        self._check_value()
        self._check_entry_equal_exit()
        self._check_entry_exit_location("ENTRY")
        self._check_entry_exit_location("EXIT")
        self._check_log_out_same()
        self._check_missing_keys()

    def _check_key(self) -> None:
        """Splits each line into key/value and
            filters out unrecognized keys."""
        for line in self.valid_lines:
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if key in KeyValueValidator.VALID_KEYS:
                self.valid_dict[key] = value
            else:
                self.non_valid_key[key] = value

    def _check_value(self) -> None:
        """Dispatches each key to its specific value validator."""
        for key in list(self.valid_dict.keys()):
            if key in {"WIDTH", "HEIGHT"}:
                self._check_width_height(key, self.valid_dict[key])
            elif key in {"ENTRY", "EXIT"}:
                self._check_entry_exit(key, self.valid_dict[key])
            elif key in {"OUTPUT_FILE", "LOG_FILE"}:
                self._check_file_key(key, self.valid_dict[key])
            elif key == "PERFECT":
                self._check_perfect(key, self.valid_dict[key])
            elif key == "SEED":
                self._check_seed(key, self.valid_dict[key])
            elif key == "MSG":
                self._check_msg(key, self.valid_dict[key])

    def _invalidate(self, key: str, value: Any) -> None:
        """Moves a key from valid_dict to non_valid_value."""
        self.non_valid_value[key] = value
        self.valid_dict.pop(key, None)

    def _check_width_height(self, key: str, value: Any) -> None:
        """Validates WIDTH and HEIGHT as integers >= 5."""
        try:
            int_value = int(value)
            if int_value < 7 and key == "HEIGHT":
                self.errors[key] = (f"{key} must be an integer >= 7 to print "
                                    "the number inside the maze")
                self._invalidate(key, value)
            elif int_value < 9 and key == "WIDTH":
                self.errors[key] = (f"{key} must be >= 9 to print the number "
                                    "inside the maze")
                self._invalidate(key, value)
            else:
                self.valid_dict[key] = int_value
        except ValueError:
            if not self.errors.get(key):
                self.errors[key] = f"{key} must be an integer"
            self._invalidate(key, value)

    def _check_entry_exit(self, key: str, value: Any) -> None:
        """Validates ENTRY and EXIT as 'row,col' integer coordinate pairs."""
        try:
            raw = str(value)
            if "," not in raw:
                raise ValueError

            row_str, col_str = raw.split(",", 1)
            row_int = int(row_str.strip())
            col_int = int(col_str.strip())

            if row_int < 0 or col_int < 0:
                self.errors[key] = (f"{key} coordinates must be non-negative "
                                    "integers")
                raise ValueError

            self.valid_dict[key] = (row_int, col_int)
        except (ValueError, TypeError):
            if not self.errors.get(key):
                self.errors[key] = f"{key} must be in the format 'x,y'"
            self._invalidate(key, value)

    def _check_perfect(self, key: str, value: Any) -> None:
        """Validates PERFECT as a boolean-like string
            ('true' or 'false') and can be 0 an 1."""
        normalized_str = str(value).strip().upper()
        if normalized_str == "TRUE":
            self.valid_dict[key] = True
            return
        if normalized_str == "FALSE":
            self.valid_dict[key] = False
            return

        if normalized_str.isdigit():
            normalized_int = int(normalized_str)
            if normalized_int == 1:
                self.valid_dict[key] = True
            elif normalized_int == 0:
                self.valid_dict[key] = False
            else:
                self._invalidate(key, value)
            return
        self.errors[key] = f"{key} must be 'true', 'false', 1, or 0 "
        f"cant be {normalized_str}"
        self._invalidate(key, value)

    def _check_file_key(self, key: str, value: Any) -> None:
        """Validates OUTPUT_FILE and LOG_FILE by checking write access."""
        file = FileValidator(str(value), "w")
        if not file.is_validate:
            self.errors[key] = f"{file.error[0]} for {key}"
            self._invalidate(key, value)

    def _check_seed(self, key: str, value: Any) -> None:
        """Validates SEED as a non-negative integer."""
        try:
            int_value = int(value)
            self.valid_dict[key] = int_value
        except (ValueError, TypeError):
            self.errors[key] = f"{key} must be an integer"
            self._invalidate(key, value)

    def _check_msg(self, key: str, value: Any) -> None:
        try:
            int_value = int(value)
            if int_value < 0 or int_value > 99:
                raise ValueError
            self.valid_dict[key] = int_value
        except (ValueError, TypeError):
            self.errors[key] = f"{key} must be an integer between 0 and 99"
            self._invalidate(key, value)

    def _check_entry_equal_exit(self) -> None:
        """Invalidates ENTRY and EXIT if they point to the same cell."""
        try:
            if self.valid_dict["ENTRY"] == self.valid_dict["EXIT"]:
                self._invalidate("ENTRY", self.valid_dict.get("ENTRY"))
                self._invalidate("EXIT", self.valid_dict.get("EXIT"))
                self.errors["EQUALITY"] = ("ENTRY and EXIT cannot be the same "
                                           "cell")
        except KeyError:
            pass

    def _check_entry_exit_location(self, key: str) -> None:
        try:
            row, col = self.valid_dict[key]
            if row >= self.valid_dict["HEIGHT"]:
                raise ValueError
            if col >= self.valid_dict["WIDTH"]:
                raise ValueError
        except KeyError:
            pass
        except ValueError:
            self.errors[key] = (f"{key} coordinates must be within the maze "
                                "dimensions")
            self._invalidate(key, self.valid_dict[key])

    def _check_log_out_same(self) -> None:
        try:
            log = self.valid_dict["LOG_FILE"]
            out = self.valid_dict["OUTPUT_FILE"]
            if log == out:
                raise ValueError
        except ValueError:
            self.errors["FILE_CONFLICT"] = ("LOG_FILE and OUTPUT_FILE cannot "
                                            "be the same file")
            self._invalidate("LOG_FILE", self.valid_dict["LOG_FILE"])
        except KeyError:
            pass

    def _check_missing_keys(self) -> None:
        """Sets is_validated to False if any mandatory key is absent."""
        self.missing_keys = [
            key for key in KeyValueValidator.MANDATORY_KEYS
            if key not in self.valid_dict
        ]
        if self.missing_keys:
            self.is_validated = False
