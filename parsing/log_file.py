from typing import Any
from styles import Color, Style


class LogFile:
    """
    Writes parsing logs either to a file or to the terminal.

    If a log file path is provided, the full report is written there.
    If no log file is given, only errors are printed to the terminal.

    Attributes:
        file (str | None): Path to the log file, or None for terminal output.
        comments (list[str]): Comments stripped from the config file.
        invalid_lines (list[str]): Lines with no '=' sign.
        report (dict[str, int]): Summary counts from LineValidator.
        non_valid_key (dict[str, str]): Unrecognized keys.
        non_valid_value (dict[str, Any]): Keys with invalid values.
        missing_keys (list[str]): Mandatory keys that were absent.
    """

    SEPARATOR = "=" * 50

    def __init__(
        self,
        file: str | None,
        comments: list[str],
        invalid_lines: list[str],
        report: dict[str, int],
        non_valid_key: dict[str, str],
        non_valid_value: dict[str, Any],
        missing_keys: list[str],
        valid_data: dict[str, str | int],
        display: bool,
        errors: dict[str, str]
    ) -> None:
        self.file = file
        self.comments = comments
        self.invalid_lines = invalid_lines
        self.report = report
        self.non_valid_key = non_valid_key
        self.non_valid_value = non_valid_value
        self.missing_keys = missing_keys
        self.valid_data = valid_data
        self.display = display
        self.errors = errors
        if self.file:
            self._write_to_file()
        if self.display:
            self._print_to_terminal()
            self._print_valid_data()

    def _write_to_file(self) -> None:
        """Writes the full report to the log file."""
        if self.file is None:
            return
        with open(self.file, "a") as f:
            self._section(f, "LOGS")
            for report_key, report_value in self.report.items():
                print(f"{report_key}: {report_value}", file=f)

            self._section(f, "COMMENTS")
            for comment in self.comments:
                print(comment, file=f)

            self._section(f, "INVALID LINES (no '=' sign)")
            for line in self.invalid_lines:
                print(line, file=f)

            self._section(f, "UNKNOWN KEYS")
            for bad_key, bad_value in self.non_valid_key.items():
                print(f"{bad_key} = {bad_value}", file=f)

            self._section(f, "INVALID VALUES")
            for invalid_key, invalid_value in self.non_valid_value.items():
                print(f"{invalid_key} = {invalid_value}", file=f)

            self._section(f, "MISSING MANDATORY KEYS")
            for missing_key in self.missing_keys:
                print(f"{missing_key} is missing", file=f)

    def _section(self, f: Any, title: str) -> None:
        """Prints a section header to the file."""
        print(f"\n{self.SEPARATOR}", file=f)
        print(f"  {title}", file=f)
        print(f"{self.SEPARATOR}\n", file=f)

    def _print_to_terminal(self) -> None:
        """Prints only errors to the
            terminal when no log file is configured."""
        has_errors = (
            self.non_valid_key
            or self.non_valid_value
            or self.missing_keys
        )
        if not has_errors:
            return

        print(f"\n{Style.BOLD}{Color.YELLOW}{'=' * 90}{Style.RESET}")
        print(f"{Style.BOLD}{Color.YELLOW}  A-Maze-ing — Config "
              f"Warnings{Style.RESET}")
        print(f"{Style.BOLD}{Color.YELLOW}{'=' * 90}{Style.RESET}")

        for key, value in self.non_valid_key.items():
            print(f"  {Color.BG_YELLOW}{Color.WHITE}{Style.BOLD} WARN "
                  f"{Style.RESET} Unknown key — {key}: {value}")

        for key, value in self.errors.items():
            print(f"  {Color.BG_YELLOW}{Color.WHITE}{Style.BOLD} WARN"
                  f" {Style.RESET} Invalid value — {value}")

        print()

    def _print_valid_data(self) -> None:
        print(f"\n{Style.BOLD}{Color.GREEN}{'=' * 90}{Style.RESET}")
        print(f"{Style.BOLD}{Color.GREEN}  A-Maze-ing — "
              f"Valid Data{Style.RESET}")
        print(f"{Style.BOLD}{Color.GREEN}{'=' * 90}{Style.RESET}")

        for key, value in self.valid_data.items():
            print(f"  {Color.BG_GREEN}{Color.WHITE}{Style.BOLD} SUCC "
                  f"{Style.RESET} Valid Data — {key}: {value}")
