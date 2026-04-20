from display.styles import Color
from typing import List, Tuple

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class DisplayMaze():
    def __init__(self,
                 grid: List[List[int]],
                 grid_flag: List[List[int]],
                 entry: Tuple[int, int],
                 exit: Tuple[int, int],
                 display_path: bool,
                 wall_color: str,
                 paths_color: str,
                 number_color: str,
                 entry_color: str,
                 exit_color: str,
                 border_color: str) -> None:

        self.grid: List[List[int]] = grid
        self.grid_flags: List[List[int]] = grid_flag
        self.height: int = len(grid)
        self.width: int = len(grid[0])
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit
        self.wall: str = f"{wall_color}  {Color.RESET}"
        self.paths: str = f"{paths_color}  {Color.RESET}"
        self.number: str = f"{number_color}  {Color.RESET}"
        self.border: str = f"{border_color}  {Color.RESET}"
        self.entry_wall: str = f"{entry_color}  {Color.RESET}"
        self.exit_wall: str = f"{exit_color}  {Color.RESET}"
        self.path_wall: str = f"{paths_color}🔴{Color.RESET}"
        self.display_path: bool = display_path
        self.display_maze()

    def display_maze(self) -> None:

        total_width = (self.width * 2) + 3

        print(self.border * total_width)

        for i in range(self.height):
            top = self.border
            mid = self.border

            for j in range(self.width):
                cell = self.grid[i][j]
                if self.grid_flags[i][j] == 1:
                    top += (self.wall if cell & NORTH
                            else self.number) + self.wall
                else:
                    top += self.wall + (self.wall if cell & NORTH else
                                        self.paths)

            top += self.wall + self.border

            print(top)

            for j in range(self.width):
                cell = self.grid[i][j]
                if (i, j) == self.entry:
                    mid += (self.wall if cell & WEST else
                            self.paths) + self.entry_wall
                elif (i, j) == self.exit:
                    mid += (self.wall if cell & WEST else
                            self.paths) + self.exit_wall
                elif (self.display_path and (self.grid_flags[i][j] == 5)):
                    mid += (self.wall if cell & WEST
                            else self.paths) + self.path_wall
                elif self.grid_flags[i][j] == 1:
                    mid += (self.wall if cell & WEST
                            else self.paths) + self.number
                else:
                    mid += (self.wall if cell & WEST else
                            self.paths) + self.paths

            mid += self.wall + self.border

            print(mid)

        bot = self.border
        for j in range(self.width):
            cell = self.grid[self.height - 1][j]
            bot += self.wall + (self.wall if cell & SOUTH else self.paths)

        bot += self.wall + self.border

        print(bot)

        print(self.border * total_width)
