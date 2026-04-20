from typing import Any


class DataValidator():
    """
    Safety layer for MazeGenerator input.

    Ensures that even if data is injected directly into the maze generator,
    all fields are clean and typed. Only mandatory maze fields are processed.
    Accepts values as raw strings, integers, booleans, or tuples.

    Attributes:
        width (int | None): Maze width, must be >= 5.
        height (int | None): Maze height, must be >= 5.
        entry (tuple[int, int] | None): Entry cell coordinates.
        exit (tuple[int, int] | None): Exit cell coordinates.
        output_file (str | None): Path to the output file.
        perfect (bool | None): Whether the maze must be perfect.
        seed (int | None): Random seed, optional.
        valid (bool): False if any mandatory field is None.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.data: dict[str, Any] = data
        self.width: int | None = None
        self.height: int | None = None
        self.entry: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.output_file: str | None = None
        self.perfect: bool | None = None
        self.seed: int | None = None
        self.msg: int = 42
        self.valid: bool = True
        self._validate()

    def _validate(self) -> None:
        """Runs all field validators in order."""
        self._upper_keys()
        self._validate_width()
        self._validate_height()
        self._validate_entry()
        self._validate_exit()
        self._validate_entry_exit()
        self._validate_output_file()
        self._validate_perfect()
        self._validate_seed()
        self._validate_msg()
        self._validate_entry_exit_range()
        self._check_all()

    def _upper_keys(self) -> None:
        upper_dict = {}
        for key, value in self.data.items():
            if isinstance(value, str):
                value = value.strip()
            upper_dict[key.upper().strip()] = value
        self.data = upper_dict

    def _validate_width(self) -> None:
        """Validates WIDTH as an integer >= 5."""
        try:
            value = int(self.data["WIDTH"])
            self.width = value if value >= 9 else None
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_height(self) -> None:
        """Validates HEIGHT as an integer >= 5."""
        try:
            value = int(self.data["HEIGHT"])
            self.height = value if value >= 7 else None
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_entry(self) -> None:
        """Validates ENTRY as an (x, y) pair — accepts tuples only."""
        try:
            value = self.data["ENTRY"]
            if isinstance(value, tuple) and len(value) == 2:
                if value[0] < 0 or value[1] < 0:
                    self.data["ENTRY"] = None
                    raise ValueError
                self.entry = (int(value[0]), int(value[1]))
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_exit(self) -> None:
        """Validates EXIT as an (x, y) pair — accepts tuples only."""
        try:
            value = self.data["EXIT"]
            if isinstance(value, tuple) and len(value) == 2:
                if value[0] < 0 or value[1] < 0:
                    self.data["EXIT"] = None
                    raise ValueError
                self.exit = (int(value[0]), int(value[1]))
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_entry_exit(self) -> None:
        """Invalidates both ENTRY and EXIT if they point to the same cell."""
        if self.entry is None or self.exit is None:
            return
        if self.entry is not None and self.exit is not None:
            if self.entry == self.exit:
                self.entry = None
                self.exit = None

    def _validate_output_file(self) -> None:
        """Validates OUTPUT_FILE by attempting to open it in append mode."""
        try:
            path = str(self.data["OUTPUT_FILE"])
            with open(path, "a"):
                pass
            self.output_file = path
        except (KeyError, TypeError):
            pass

    def _validate_perfect(self) -> None:
        """Validates PERFECT as a boolean —
            accepts bool, 'true'/'false', or 0/1."""
        try:
            value = self.data["PERFECT"]
            if isinstance(value, bool):
                self.perfect = value
                return
            if isinstance(value, str):
                if value.isdigit():
                    value = int(value)
            if isinstance(value, int):
                if value == 0:
                    self.perfect = False
                elif value == 1:
                    self.perfect = True
                else:
                    return
            elif isinstance(value, str):
                if value.upper() == "TRUE":
                    self.perfect = True
                elif value.upper() == "FALSE":
                    self.perfect = False
            else:
                return
        except (KeyError, TypeError):
            pass

    def _validate_seed(self) -> None:
        """Validates SEED as a non-negative integer, optional field."""
        try:
            value = int(self.data["SEED"])
            self.seed = value
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_msg(self) -> None:
        """Validates MSG as an integer between 0 and 99"""
        try:
            value = int(self.data["MSG"])
            self.msg = value if value >= 0 and value <= 99 else 42
        except (KeyError, ValueError, TypeError):
            pass

    def _validate_entry_exit_range(self) -> None:
        try:
            if self.width is None or self.height is None:
                return
            if self.entry is not None:
                x_e, y_e = self.entry
                if x_e >= self.height or y_e >= self.width:
                    self.entry = None
            if self.exit is not None:
                x_x, y_x = self.exit
                if x_x >= self.height or y_x >= self.width:
                    self.exit = None
        except (KeyError, TypeError):
            pass

    def _check_all(self) -> None:
        """Sets valid to False if any mandatory field is None."""
        mandatory: list[Any] = [
            self.width, self.height,
            self.entry, self.exit,
            self.output_file, self.perfect,
        ]
        for element in mandatory:
            if element is None:
                self.valid = False
