class LineValidator():
    """
    Validates and filters raw lines read from a config file.

    Attributes:
        lines (list[str]): Working list of lines, progressively cleaned.
        valid_lines (list[str]): Final list of valid 'KEY=VALUE' lines.
        invalid_lines (list[str]): Lines that had no '=' sign.
        comments (list[str]): Comment content stripped from lines.
        report (dict[str, int]): Summary count of empty
            lines, comments, and invalid lines.
    """

    def __init__(self, lines: list[str]) -> None:
        self.lines: list[str] = self._strip_lines(lines)
        self.valid_lines: list[str] = []
        self.invalid_lines: list[str] = []
        self.comments: list[str] = []
        self.report: dict[str, int] = {
            "empty_lines": 0,
            "comments": 0,
            "nosign": 0,
        }
        self._validate()

    def _validate(self) -> None:
        """Runs all validation steps in order."""
        self._remove_empty_lines()
        self._remove_comments()
        self._remove_nosign()

    def _strip_lines(self, lines: list[str]) -> list[str]:
        striped_Lines = []
        for line in lines:
            striped_Lines.append(line.strip())
        return striped_Lines

    def _remove_empty_lines(self) -> None:
        """Removes empty lines and records their count in the report."""
        self.report["empty_lines"] = self.lines.count("")
        selflines = []
        for line in self.lines:
            if line != "":
                selflines.append(line)
        self.lines = selflines

    def _remove_comments(self) -> None:
        """Strips inline and full-line comments, keeping any
            valid content before '#'."""
        cleaned: list[str] = []
        for line in self.lines:
            if "#" in line:
                line, comment = line.split("#", 1)
                line = line.strip()
                self.report["comments"] += 1
                self.comments.append(comment.strip())
            if line:
                cleaned.append(line)
        self.lines = cleaned

    def _remove_nosign(self) -> None:
        """Separates lines with '=' (valid) from those without (invalid)."""
        for line in self.lines:
            if "=" in line:
                self.valid_lines.append(line)
            else:
                self.invalid_lines.append(line)
                self.report["nosign"] += 1
