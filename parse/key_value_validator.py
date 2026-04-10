from .file_validator import FileValidator


class KeyValueValidator():
    VALID_DATA = ["WIDTH",
                  "HEIGHT",
                  "EXIT",
                  "ENTRY",
                  "OUTPUT_FILE",
                  "PERFECT",
                  "SEED",
                  "LOG_FILE"]

    MANDATORY_KEYS = ["WIDTH",
                      "HEIGHT",
                      "ENTRY",
                      "EXIT",
                      "OUTPUT_FILE",
                      "PERFECT"]

    def __init__(self, valid_lines):
        self.valid_lines = valid_lines
        self.valid_dict = {}
        self.non_valid_key = {}
        self.non_valid_value = {}
        self.is_validated = True
        self.missing_keys = []
        self._validate()

    def _validate(self):
        self._check_key()
        self._check_value()
        self._check_all()

    def _check_key(self):
        for line in self.valid_lines:
            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            if key in KeyValueValidator.VALID_DATA:
                self.valid_dict = self.valid_dict | {key: value}
            else:
                self.non_valid_key = self.non_valid_key | {key: value}

    def _check_value(self):
        for key in list(self.valid_dict.keys()):
            if key == "WIDTH" or key == "HEIGHT":
                self._check_width_height(key, self.valid_dict[key])
            elif key == "ENTRY" or key == "EXIT":
                self._check_entry_exit(key, self.valid_dict[key])
            elif key == "OUTPUT_FILE" or key == "LOG_FILE":
                self._check_output_file_log_file(key, self.valid_dict[key])
            elif key == "PERFECT":
                self._check_perfect(key, self.valid_dict[key])
            elif key == "SEED":
                self._check_seed(key, self.valid_dict[key])

    def _check_width_height(self, key, value):
        try:
            value = int(value)
            if value < 5:
                self.non_valid_value = self.non_valid_value | {key: value}
                del self.valid_dict[key]
            else:
                self.valid_dict[key] = value
        except ValueError:
            del self.valid_dict[key]
            self.non_valid_value = self.non_valid_value | {key: value}

    def _check_entry_exit(self, key, value):
        try :
            if "," in value:
                value1, value2 = value.split(",", 1)
                value1 = int(value1)
                value2 = int(value2)
                self.valid_dict[key] = (value1, value2)
            else:
                self.non_valid_value = self.non_valid_value | {key: value}
                del self.valid_dict[key]
        except ValueError:
            self.non_valid_value = self.non_valid_value | {key: value}
            del self.valid_dict[key]

    def _check_perfect(self, key, value):
        value_tmp = value.upper()
        if value_tmp == "True" or value_tmp == "False":
            return
        if isinstance(value_tmp, int):
            if value_tmp == 0:
                self.valid_dict[key] = "False"
            elif value_tmp == 1:
                self.valid_dict[key] = "True"
            else:
                self.non_valid_value = self.non_valid_value | {key: value}
                del self.valid_dict[key]

    def _check_output_file_log_file(self, key, value):
        file = FileValidator(self.valid_dict[key], "w")
        if file.is_validate == False:
            self.non_valid_value = self.non_valid_value | {key: value}
            del self.valid_dict[key]

    def _check_seed(self, key, value):
        try :
            value = int(value)
            self.valid_dict = self.valid_dict | {key: value}
        except ValueError:
            self.non_valid_value = self.non_valid_value | {key: value}
            del self.valid_dict[key]

    def _check_entry_equal_exit(self):
        try:
            x_e, y_e = self.valid_dict["EXIT"]
            x_s, y_s = self.valid_dict["ENTRY"]
            if x_e == x_s and y_e == y_s:
                self.non_valid_value = self.non_valid_value | {"EXIT": (x_e, y_e)}
                self.non_valid_value = self.non_valid_value | {"ENTRY": (x_s, y_s)}
                del self.valid_dict["ENTRY"]
                del self.valid_dict["EXIT"]
        except (KeyError, ValueError):
            pass

    def _check_all(self):
        for element in KeyValueValidator.MANDATORY_KEYS:
            if element not in list(self.valid_dict.keys()):
                self.is_validated = False
                self.missing_keys.append(element)
