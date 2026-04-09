VALID_DATA = ["WIDTH",
                "HEIGHT",
                "EXIT",
                "ENTRY",
                "OUTPUT_FILE",
                "PERFECT",
                "SEED",
                "LOG_FILE"]

class HundleInput():
    def __init__(self, data):
        self.data = data
        self.width = None
        self.height = None
        self.entry = None
        self.exit = None
        self.output_file = None
        self.perfect = None
        self.seed = None
        self.valid = True
        self._validate()

    def _validate(self):
        self._upper_all()
        self._validate_height()
        self._validate_width()
        self._validate_entry()
        self._validate_exit()
        self._validate_output_file()
        self._validate_perfect()
        self._validate_seed()
        self._check_all()

    def _upper_all(self):
        for data in self.data:
            self.data[data.upper()] = self.data[data]
            del self.data[data]

    def _validate_width(self):
        try :
            self.data["WIDTH"] = int(self.data["WIDTH"])
        except (KeyError, ValueError):
            self.width = None

    def _validate_height(self):
        try :
            self.data["HEIGHT"] = int(self.data["HEIGHT"])
        except (KeyError, ValueError):
            self.height = None

    def _validate_entry(self):
        try :
            value1, value2 = self.data["ENTRY"].split(",", 1)
            value1 = int(value1)
            value2 = int(value2)
        except (KeyError, ValueError):
            self.entry = None

    def _validate_exit(self):
        try :
            value1, value2 = self.data["EXIT"]
            value1 = int(value1)
            value2 = int(value2)
        except (KeyError, ValueError):
            self.entry = None

    def _validate_perfect(self):
        try:
            value = self.data["PERFECT"]
            value = value.upper().strip()
            if value == "TRUE" or value == "FALSE":
                self.data["PERFECT"] = value
            elif int(value) == 1:
                self.data["PERFECT"] = "TRUE"
            elif int(value) == 0:
                self.data["PERFECT"] = "FALSE"
            else :
                self.data["PERFECT"] = None
        except (KeyError, ValueError):
            self.data["PERFECT"] = None

    def _validate_seed(self):
        try:
            self.data["SEED"] = int(self.data["SEED"])
        except (KeyError, ValueError):
            self.data["SEED"] = 42

    def _validate_output_file(self):
        try:
            with open("self.data['OUTPUT_FILE']", "w") as file:
                file.write("")
        except Exception:
            self.data["OUTPUT_FILE"] = None

    def _check_all(self):
        for data in self.data:
            if self.data[data] == None and data not in VALID_DATA:
                self.valid = False
                break
