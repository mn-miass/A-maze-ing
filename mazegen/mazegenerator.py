from mazegen.data_validator import DataValidator
from mazegen.map_generation import MapGenerator
from mazegen.hunt_and_kill import HuntAndKill
from mazegen.path_finder import PathFinder
from typing import Any
import sys
import random


class MazeGenerator():
    """
    Main orchestrator for the maze generation pipeline.

    Takes a raw config dictionary, validates it, generates the base map,
    runs the Hunt-and-Kill algorithm, and hands the result to the display.

    Pipeline:
        raw data → HandleInput → MapGenerator → HuntAndKill → MazeDisplay

    Attributes:
        input (HandleInput): Validated input data.
        map (MapGenerator): Base flag and hex grids.
        maze (HuntAndKill): Generated maze walls.
        display (MazeDisplay): Terminal renderer.
        valid (bool): False if input validation failed.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.input: DataValidator | None = None
        self.map: MapGenerator | None = None
        self.maze: HuntAndKill | None = None
        self.path: PathFinder | None = None
        self.valid: bool = True
        self._build(data)

    def _build(self, data: dict[str, Any]) -> None:
        """
        Runs the full pipeline from raw data to display.

        Args:
            data: Raw config dictionary.
        """
        # Step 1 — validate input
        self.input = DataValidator(data)
        if not self.input.valid:
            self.valid = False
            return
        assert self.input.height is not None
        assert self.input.width is not None
        assert self.input.entry is not None
        assert self.input.exit is not None
        assert self.input.output_file is not None
        assert self.input.perfect is not None

        # Step 2 — generate base map with pattern
        self.map = MapGenerator(
            height=self.input.height,
            width=self.input.width,
            msg=self.input.msg,
            entry=self.input.entry,
            exit=self.input.exit
        )

        if self.map.valid is False:
            print("\033[41m\033[97m\033[1m [ERROR]: Cant creat the maze "
                  "entry/exit cant be in the number")
            sys.exit(1)

        # Step 3 — run Hunt-and-Kill on the grids
        self.maze = HuntAndKill(
            grid_hex=self.map.hex,
            grid_flags=self.map.flags,
            grid_dec=self.map.dec,
            height=self.input.height,
            width=self.input.width,
            seed=(self.input.seed if self.input.seed
                  is not None else random.random()),
            perfect=self.input.perfect
        )

        self.path = PathFinder(
            entry=self.input.entry,
            exit=self.input.exit,
            grid_dec=self.map.dec,
            grid_flags=self.map.flags
        )
        with open(self.input.output_file, "w") as f:
            for i in range(self.input.height):
                row: str = ""
                for j in range(self.input.width):
                    row += str(self.maze.grid_hex[i][j])
                print(row, file=f, flush=True)
            print("", file=f)
            print(f"{self.input.entry[0]},{self.input.entry[1]}", file=f)
            print(f"{self.input.exit[0]},{self.input.exit[1]}", file=f)
            print(f"{self.path.direction}", file=f)
