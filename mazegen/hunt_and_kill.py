import random
from .hex_bin import decimal_to_hexa


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class HuntAndKill():
    """
    Generates a perfect maze using the Hunt-and-Kill algorithm.

    Starts from (0, 0) and carves paths by randomly walking to unvisited
    neighbours. When stuck, hunts row by row for an unvisited cell that
    has at least one visited neighbour, then resumes from there.

    Cells in grid_flags use three states:
        0 = unvisited
        1 = pattern cell (blocked, not carveable)
        2 = visited

    Attributes:
        grid_hex (list[list[str]]): Hex representation of the maze.
        grid_flags (list[list[int]]): Visitation state grid.
        grid_dec (list[list[int]]): Decimal wall values grid.
        height (int): Number of rows.
        width (int): Number of columns.
        rrs (random.Random): Seeded random instance.
    """

    def __init__(
        self,
        grid_hex: list[list[str]],
        grid_flags: list[list[int]],
        grid_dec: list[list[int]],
        height: int,
        width: int,
        seed: float,
        perfect: bool
    ) -> None:
        self.grid_hex: list[list[str]] = grid_hex
        self.grid_flags: list[list[int]] = grid_flags
        self.grid_dec: list[list[int]] = grid_dec
        self.height: int = height
        self.width: int = width
        self.rrs: random.Random = random.Random(seed)
        self.perfect = perfect
        self._generate()

    def _generate(self) -> None:
        """
        Runs the Hunt-and-Kill generation loop.

        Alternates between a random-walk phase (kill) and a
        row-by-row scan phase (hunt) until all reachable cells
        are visited.
        """
        current_x = 0
        current_y = 0
        self.grid_flags[current_x][current_y] = 2

        while True:
            neighbours = self._unvisited_neighbour((current_x, current_y))
            if neighbours:
                next_x, next_y, wall_c, wall_n = \
                    self._random_neighbour(neighbours)
                self._carve(
                    (current_x, current_y), (next_x, next_y),
                    wall_c, wall_n
                )
                current_x = next_x
                current_y = next_y
            else:
                # Hunt phase — scan for unvisited cell with visited neighbour
                found = False
                for x in range(self.height):
                    for y in range(self.width):
                        if self.grid_flags[x][y] == 0:
                            neighbours = self._visited_neighbour((x, y))
                            if neighbours:
                                next_x, next_y, wall_c, wall_n = \
                                    self._random_neighbour(neighbours)
                                self._carve(
                                    (next_x, next_y), (x, y),
                                    wall_n, wall_c
                                )
                                current_x = x
                                current_y = y
                                found = True
                                break  # break inner loop
                    if found:
                        break  # break outer loop
                if not found:
                    break  # no unvisited cells left — done
        if not self.perfect:
            self._make_imperfect()
        self._hex_grid()

    def _unvisited_neighbour(self, cell: tuple[int, int]) \
            -> list[tuple[int, int, int, int]]:

        """
        Returns all unvisited (state 0) neighbours of a cell.

        Args:
            cell: (row, col) of the current cell.

        Returns:
            List of (row, col, wall_from_current, wall_from_neighbour).
        """
        x, y = cell
        valid = []
        if (x > 0 and
                self.grid_flags[x - 1][y] == 0):
            valid.append((x - 1, y, NORTH, SOUTH))
        if (y > 0 and
                self.grid_flags[x][y - 1] == 0):
            valid.append((x, y - 1, WEST, EAST))
        if (x < self.height - 1 and
                self.grid_flags[x + 1][y] == 0):
            valid.append((x + 1, y, SOUTH, NORTH))
        if (y < self.width - 1 and
                self.grid_flags[x][y + 1] == 0):
            valid.append((x, y + 1, EAST, WEST))
        return valid

    def _visited_neighbour(self, cell: tuple[int, int]) \
            -> list[tuple[int, int, int, int]]:
        """
        Returns all visited (state 2) neighbours of a cell.

        Args:
            cell: (row, col) of the current cell.

        Returns:
            List of (row, col, wall_from_current, wall_from_neighbour).
        """
        x, y = cell
        valid = []
        if (x > 0 and self.grid_flags[x - 1][y] == 2 and
                self.grid_dec[x - 1][y] & SOUTH):
            valid.append((x - 1, y, NORTH, SOUTH))
        if (y > 0 and self.grid_flags[x][y - 1] == 2 and
                self.grid_dec[x][y - 1] & EAST):
            valid.append((x, y - 1, WEST, EAST))
        if (x < self.height - 1 and self.grid_flags[x + 1][y] == 2 and
                self.grid_dec[x + 1][y] & NORTH):
            valid.append((x + 1, y, SOUTH, NORTH))
        if (y < self.width - 1 and self.grid_flags[x][y + 1] == 2 and
                self.grid_dec[x][y + 1] & WEST):
            valid.append((x, y + 1, EAST, WEST))
        return valid

    def _random_neighbour(self, neighbours: list[tuple[int, int, int, int]]) \
            -> tuple[int, int, int, int]:
        """
        Picks a random neighbour from the given list.

        Args:
            neighbours: List of neighbour tuples.

        Returns:
            A randomly chosen neighbour tuple.
        """
        return self.rrs.choice(neighbours)

    def _carve(
        self,
        cell: tuple[int, int],
        neighbour: tuple[int, int],
        cell_wall: int,
        neighbour_wall: int,
    ) -> None:
        """
        Removes the wall between two cells and marks the neighbour as visited.

        Args:
            cell: (row, col) of the source cell.
            neighbour: (row, col) of the target cell.
            cell_wall: Wall bitmask to remove from source cell.
            neighbour_wall: Wall bitmask to remove from target cell.
        """
        x_c, y_c = cell
        x_n, y_n = neighbour
        self.grid_dec[x_c][y_c] -= cell_wall
        self.grid_dec[x_n][y_n] -= neighbour_wall
        self.grid_flags[x_n][y_n] = 2

    def _make_imperfect(self) -> None:
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                if self.grid_flags[i][j] == 1:
                    continue
                if self.height < 10 and self.width < 10:
                    value = 0.50
                else:
                    value = 0.1317
                if self.rrs.random() < value:
                    n = self._visited_neighbour((i, j))
                    if n:
                        n_x, n_y, w_c, w_n = self._random_neighbour(n)
                        self._carve((i, j), (n_x, n_y), w_c, w_n)

    def _hex_grid(self) -> None:
        self.grid_hex = decimal_to_hexa(self.grid_dec)
