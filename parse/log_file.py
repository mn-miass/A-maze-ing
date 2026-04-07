class LogFile():
    def __init__(self,
                 file,
                 comments,
                 invalid_lines_no_sign,
                 final_report,
                 non_valid_key,
                 non_valid_value,
                 missing_elements
                 ):
        self.file = file
        self.comments = comments
        self.invalid_lines_no_sign = invalid_lines_no_sign
        self.final_report = final_report
        self.non_valid_key = non_valid_key
        self.non_valid_value = non_valid_value
        self.missing_elements = missing_elements
        self._printlogs()

    def _printlogs(self):
        with open(self.file, "a") as f:
            print("\n======================LOGS=========================\n", file=f)
            for key in self.final_report:
                print(f"{key}: {self.final_report[key]}", file=f)
            self._printcomments(f)
            self._printinvalid_lines(f)
            self._printnon_valid_data(f)
            self._printnon_valid_value(f)
            self._printmissing(f)

    def _printcomments(self, f):

        print("\n======================COMMENTS=========================\n", file=f)
        for comment in self.comments:
            print(f"{comment}", file=f)

    def _printinvalid_lines(self, f):
        print("\n=====================INVALID LINES======================\n", file=f)
        for invalid in self.invalid_lines_no_sign:
            print(f"{invalid}", file=f)


    def _printnon_valid_data(self, f):
        print("\n======================INVALID DATA=======================\n", file=f)
        for invalid in self.non_valid_key:
            print(f"{invalid}", file=f)

    def _printnon_valid_value(self, f):
        print("\n=======================INVALID VALUE========================\n", file=f)
        for invalid in self.non_valid_value:
            print(f"{invalid} = {self.non_valid_value[invalid]}", file=f)

    def _printmissing(self,f):
        print("\n=======================MISSING========================\n", file=f)
        for invalid in self.missing_elements:
            print(f"{invalid} is missing", file=f)
