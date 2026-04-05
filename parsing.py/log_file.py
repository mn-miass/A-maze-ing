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
        self.print_logs()

    def print_logs(self):
        with open(self.file, "w") as f:
            print("\n======================LOGS=========================\n", file=f)
            for key in self.final_report:
                print(f"{key}: {self.final_report[key]}", file=f)
            self.print_comments(f)
            self.print_invalid_lines(f)
            self.print_non_valid_data(f)
            self.print_missing(f)

    def print_comments(self, f):

        print("\n======================COMMENTS=========================\n", file=f)
        for comment in self.comments:
            print(f"{comment}", file=f)

    def print_invalid_lines(self, f):
        print("\n=====================INVALID LINES======================\n", file=f)
        for invalid in self.invalid_lines_no_sign:
            print(f"{invalid}", file=f)


    def print_non_valid_data(self, f):
        print("\n======================INVALID DATA=======================\n", file=f)
        for invalid in self.non_valid_key:
            print(f"{invalid}", file=f)

    def print_non_valid_value(self, f):
        print("\n=======================INVALID VALUE========================\n", file=f)
        for invalid in self.non_valid_value:
            print(f"{invalid} = {self.non_valid_value[invalid]}", file=f)

    def print_missing(self,f):
        print("\n=======================MISSING========================\n", file=f)
        for invalid in self.missing_elements:
            print(f"{invalid} is missing", file=f)
