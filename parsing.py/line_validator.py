class LineValidator():
    def __init__(self, lines):
        self.valid_lines = lines
        self.invalid_lines_no_sign = []
        self.comments = []
        self.final_report = {}
        self._validate()

    def _validate(self):
        self._strip_lines()
        self._emptylines_removal()
        self._comment_remove()
        self._nosign_removal()
        self._strip_lines()

    def _strip_lines(self):
        self.valid_lines = [line.strip() for line in self.valid_lines]

    def _emptylines_removal(self):
        self.final_report["empty_lines"] = self.valid_lines.count("")
        self.valid_lines = [line for line in self.valid_lines if line != ""]

    def _comment_remove(self):
        self.final_report["comments"] = 0
        no_comment = []
        for line in self.valid_lines:
            if "#" in line:
                line, comment = line.split("#", 1)
                self.final_report["comments"] += 1
                self.comments.append(comment)
            if line:
                no_comment.append(line)
        self.valid_lines= no_comment

    def _nosign_removal(self):
        self.final_report["nosign"] = 0
        with_sign = []
        for line in self.valid_lines:
            if "=" in line:
                with_sign.append(line)
            else:
                self.invalid_lines_no_sign.append(line)
                self.final_report["nosign"] += 1
        self.valid_lines = with_sign
