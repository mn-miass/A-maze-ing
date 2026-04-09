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
        self.msg = None
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
        self._validate_msg()
        self._validate_entry_exit()
        self._check_all()

    def _upper_all(self):
        valid_data = {str(k).upper(): v for k, v in self.data.items()}
        self.data = valid_data

    def _validate_width(self):
        try :
            self.width = int(self.data["WIDTH"])
            if self.width < 5:
                self.width = None
        except (KeyError, ValueError):
            pass

    def _validate_height(self):
        try :
            self.height = int(self.data["HEIGHT"])
            if self.height < 5:
                self.height = None
        except (KeyError, ValueError):
            pass

    def _validate_entry(self):
        try :
            value1, value2 = self.data["ENTRY"]
            value1 = int(value1)
            value2 = int(value2)
            self.entry = (value1, value2)
        except (KeyError, ValueError):
            pass

    def _validate_exit(self):
        try :
            value1, value2 = self.data["EXIT"]
            value1 = int(value1)
            value2 = int(value2)
            self.exit = (value1, value2)
        except (KeyError, ValueError):
            pass

    def _validate_perfect(self):
        try:
            value = self.data["PERFECT"]
            value = value.upper().strip()
            if value == "TRUE" or value == "FALSE":
                self.perfect = value
            elif int(value) == 1:
                self.perfect = "TRUE"
            elif int(value) == 0:
                self.perfect = "FALSE"
        except (KeyError, ValueError):
            pass

    def _validate_entry_exit(self):
        try:
            print(self.exit)
            x_e, y_e = self.exit
            x_s, y_s = self.entry
            if x_e == x_s and y_e == y_s:
                self.exit = None
                self.entry = None
        except (ValueError, TypeError):
            pass

    def _validate_seed(self):
        try:
            self.seed = int(self.data["SEED"])
        except (KeyError, ValueError):
            pass

    def _validate_output_file(self):
        try:
            with open(self.data['OUTPUT_FILE'], "w") as file:
                file.write("")
            self.output_file = self.data['OUTPUT_FILE']
        except Exception:
            pass

    def _validate_msg(self):
        try:
            self.msg = int(self.data["MSG"])
            if self.msg > 99 or self.msg < 0:
                self.msg = 42
        except (KeyError, ValueError):
            self.msg = 42

    def _check_all(self):
        self.data_list = [self.width,
                          self.height,
                          self.entry,
                          self.exit,
                          self.output_file,
                          self.perfect]
        for data in self.data_list:
            if data == None :
                self.valid = False
                break
