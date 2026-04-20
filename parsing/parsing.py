import sys
from parsing.file_validator import FileValidator
from parsing.line_validator import LineValidator
from parsing.key_value_validator import KeyValueValidator
from parsing.log_file import LogFile
from styles import Color, Style
from typing import Any, Optional


class Parsing:
    """
    Orchestrates all parsing and validation steps for the config file.

    Attributes:
        file_name (str): Path to the configuration file.
        config (dict): Final validated key-value pairs ready for use.
    """

    def __init__(self, file_name: str, display: bool = True) -> None:
        self.file_name: str = file_name
        self.config: Optional[dict[str, Any]] = None
        self.display: bool = display
        self._parse()

    def _print_error(self, message: list[str]) -> None:
        """Prints a formatted error block and exits."""
        print(f"\n{Style.BOLD}{Color.RED}{'=' * 45}{Style.RESET}")
        print(f"{Style.BOLD}{Color.RED}  A-Maze-ing —"
              f" Maze Generator{Style.RESET}")
        print(f"{Style.BOLD}{Color.RED}{'=' * 45}{Style.RESET}")
        for msg in message:
            print(f"  {Color.BG_RED}{Color.WHITE}{Style.BOLD} ERROR "
                  f"{Style.RESET} {msg}")
        print()
        sys.exit(1)

    def _parse(self) -> None:
        """Runs all validation steps in order."""

        file = FileValidator(self.file_name)
        if not file.is_validate:
            self._print_error(file.error)

        lines = LineValidator(file.data)

        key_value = KeyValueValidator(lines.valid_lines)

        if "LOG_FILE" in key_value.valid_dict.keys():
            log_file = key_value.valid_dict["LOG_FILE"]
        else:
            log_file = None

        LogFile(
            file=log_file,
            comments=lines.comments,
            invalid_lines=lines.invalid_lines,
            report=lines.report,
            non_valid_key=key_value.non_valid_key,
            non_valid_value=key_value.non_valid_value,
            missing_keys=key_value.missing_keys,
            valid_data=key_value.valid_dict,
            display=self.display,
            errors=key_value.errors
        )

        if not key_value.is_validated:
            msg_list = []
            for msg in key_value.missing_keys:
                msg_list.append(f"Missing mandatory key: {msg}")
            self._print_error(msg_list)
        self.config = key_value.valid_dict
