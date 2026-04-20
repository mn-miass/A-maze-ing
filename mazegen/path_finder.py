from collections import deque
from typing import List, Optional, Tuple


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class PathFinder:
    def __init__(self,
                 entry: Tuple[int, int],
                 exit: Tuple[int, int],
                 grid_dec: List[List[int]],
                 grid_flags: List[List[int]]) -> None:
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.grid_dec: List[List[int]] = grid_dec
        self.grid_flags: List[List[int]] = grid_flags
        self.path: Optional[List[Tuple[int, int]]] = self._path_finder()
        self.direction: str = self._direction()
        self.grid_flags = self._print_path()

    def _path_finder(self) -> Optional[List[Tuple[int, int]]]:
        queue = deque([[self.entry]])
        self.grid_flags[self.entry[0]][self.entry[1]] = 3

        while queue:
            current_path = queue.popleft()
            current_pos = current_path[-1]

            if current_pos == self.exit:
                return current_path

            neighbours = self._get_neighbour(current_pos[0], current_pos[1])

            for neighbour in neighbours:
                new_path = list(current_path)
                new_path.append(neighbour)
                queue.append(new_path)
        return None

    def _get_neighbour(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbour = []
        if (x > 0 and self.grid_flags[x - 1][y] == 2 and
                self.grid_dec[x][y] & NORTH == 0):
            self.grid_flags[x-1][y] = 3
            neighbour.append((x - 1, y))
        if (x < len(self.grid_flags) - 1 and self.grid_flags[x + 1][y] == 2
                and self.grid_dec[x][y] & SOUTH == 0):
            self.grid_flags[x+1][y] = 3
            neighbour.append((x + 1, y))
        if (y > 0 and self.grid_flags[x][y - 1] == 2 and
                self.grid_dec[x][y] & WEST == 0):
            self.grid_flags[x][y-1] = 3
            neighbour.append((x, y - 1))
        if (y < len(self.grid_flags[x]) - 1 and
                self.grid_flags[x][y + 1] == 2 and
                self.grid_dec[x][y] & EAST == 0):
            self.grid_flags[x][y+1] = 3
            neighbour.append((x, y + 1))
        return neighbour

    def _direction(self) -> str:
        if self.path is None:
            return ""
        paths = ""
        for i in range(len(self.path) - 1):
            current_path = self.path[i]
            next_path = self.path[i + 1]
            x_c, y_c = current_path
            x_n, y_n = next_path
            if x_c + 1 == x_n:
                paths += "S"
            elif x_c - 1 == x_n:
                paths += "N"
            elif y_c + 1 == y_n:
                paths += "E"
            elif y_c - 1 == y_n:
                paths += "W"
        return paths

    def _print_path(self) -> List[List[int]]:
        flags = self.grid_flags
        if self.path is None:
            return flags
        paths = self.path
        for path in paths:
            x, y = path
            flags[x][y] = 5
        return flags
