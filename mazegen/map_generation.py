from mazegen.shapes import Shapes
from mazegen.hex_bin import decimal_to_hexa
from collections.abc import Callable
from typing import Tuple


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIGIT_SHAPES: dict[int, Callable[[], list[list[int]]]] = {
    0: Shapes._shape_0, 1: Shapes._shape_1,
    2: Shapes._shape_2, 3: Shapes._shape_3,
    4: Shapes._shape_4, 5: Shapes._shape_5,
    6: Shapes._shape_6, 7: Shapes._shape_7,
    8: Shapes._shape_8, 9: Shapes._shape_9,
}


class MapGenerator:
    """
    Generates the base flag grid for the maze and embeds a two-digit
    number pattern.

    The flag grid is a 2D list of integers where each cell value encodes
    wall states using NORTH, EAST, SOUTH, WEST bitmask constants.
    Cells belonging to the embedded pattern are pre-set to
    15 (all walls closed).

    Attributes:
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        msg (int): Two-digit number (0-99) to embed visually in the maze.
        flags (list[list[int]]): Raw bitmask grid.
        dec (list[list[int]]): Decimal representation of flags.
        hex (list[list[str]]): Hexadecimal representation of flags.
    """

    def __init__(self, height: int, width: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 msg: int = 42) -> None:
        self.height: int = height
        self.width: int = width
        self.msg: int = msg
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.flags: list[list[int]] = self._generate_flags()
        self._generate_msg()
        self.dec: list[list[int]] = self._generate_decimal()
        self.hex: list[list[str]] = decimal_to_hexa(self.dec)
        self.valid = True
        self._check_entry_exit_position()

    def _generate_flags(self) -> list[list[int]]:
        """Creates an empty (all zeros) bitmask grid."""
        grid = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(0)
            grid.append(row)
        return grid

    def _generate_msg(self) -> None:
        """Embeds the two-digit pattern into the flag grid if it fits."""
        pattern = self._get_pattern()
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])

        start_row = (self.height - pattern_h) // 2
        start_col = (self.width - pattern_w) // 2

        for i in range(pattern_h):
            for j in range(pattern_w):
                self.flags[start_row + i][start_col + j] = pattern[i][j]

    def _get_pattern(self) -> list[list[int]]:
        """Builds the two-digit pattern by merging the tens and ones digit
        shapes."""
        tens_grid = DIGIT_SHAPES[self.msg // 10]()
        ones_grid = DIGIT_SHAPES[self.msg % 10]()
        return self._merge(tens_grid, ones_grid)

    def _merge(self, left: list[list[int]], right: list[list[int]]) \
            -> list[list[int]]:
        """Merges two digit grids side by side with a one-column gap."""
        merged = []
        for i in range(len(left)):
            merged.append(left[i] + [0] + right[i])
        return merged

    def _check_entry_exit_position(self) -> None:
        x_e, y_e = self.entry
        x_x, y_x = self.exit
        if self.flags[x_e][y_e]:
            self.valid = False
        if self.flags[x_x][y_x]:
            self.valid = False

    def _generate_decimal(self) -> list[list[int]]:
        dec = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(15)
            dec.append(row)
        return dec
