from mazegen.data_validator import DataValidator
from mazegen.map_generation import MapGenerator
from mazegen.hunt_and_kill import HuntAndKill
from mazegen.path_finder import PathFinder
from typing import Any


def test_data_validator_valid(tmp_path: Any) -> None:
    maze_file = tmp_path / "maze.txt"
    data = {
        "WIDTH": 20,
        "HEIGHT": 15,
        "ENTRY": (0, 0),
        "EXIT": (14, 19),
        "OUTPUT_FILE": str(maze_file),
        "PERFECT": True
    }
    validator = DataValidator(data)
    assert validator.valid is True
    assert validator.width == 20
    assert validator.height == 15
    assert validator.entry == (0, 0)
    assert validator.exit == (14, 19)
    assert validator.perfect is True


def test_data_validator_invalid_dimensions() -> None:
    data = {
        "WIDTH": 8,  # Must be >= 9
        "HEIGHT": 6,  # Must be >= 7
        "ENTRY": (0, 0),
        "EXIT": (5, 5),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    validator = DataValidator(data)
    assert validator.valid is False
    assert validator.width is None
    assert validator.height is None


def test_map_generator_basic() -> None:
    # HEIGHT=7, WIDTH=9 is minimum
    mg = MapGenerator(height=7, width=9, entry=(0, 0), exit=(6, 8), msg=42)
    assert mg.height == 7
    assert mg.width == 9
    assert len(mg.flags) == 7
    assert len(mg.flags[0]) == 9
    # Check that pattern 42 is embedded
    # Pattern is roughly in the middle.
    # Just check if some flags are non-zero
    found_pattern = False
    for row in mg.flags:
        if any(cell != 0 for cell in row):
            found_pattern = True
            break
    assert found_pattern is True


def test_hunt_and_kill_generation() -> None:
    height, width = 7, 9
    mg = MapGenerator(height=height, width=width, entry=(0, 0), exit=(6, 8))

    # HuntAndKill modifies grids in place
    HuntAndKill(
        grid_hex=mg.hex,
        grid_flags=mg.flags,
        grid_dec=mg.dec,
        height=height,
        width=width,
        seed=42.0,
        perfect=True
    )

    # After generation, all reachable cells should be visited
    # (state 2) or pattern (state 1)
    for i in range(height):
        for j in range(width):
            assert mg.flags[i][j] in [1, 2]

    # Decimal grid should have some walls removed (not all 15)
    found_carved = False
    for row in mg.dec:
        if any(cell < 15 for cell in row):
            found_carved = True
            break
    assert found_carved is True


def test_path_finder() -> None:
    height, width = 7, 9
    entry, exit = (0, 0), (6, 8)
    mg = MapGenerator(height=height, width=width, entry=entry, exit=exit)
    HuntAndKill(
        grid_hex=mg.hex,
        grid_flags=mg.flags,
        grid_dec=mg.dec,
        height=height,
        width=width,
        seed=42.0,
        perfect=True
    )

    # PathFinder
    pf = PathFinder(entry=entry, exit=exit,
                    grid_dec=mg.dec, grid_flags=mg.flags)
    assert pf.path is not None
    assert pf.path[0] == entry
    assert pf.path[-1] == exit
    assert len(pf.direction) > 0
    # Direction string should only contain NSEW
    assert all(c in "NSEW" for c in pf.direction)


def test_shapes() -> None:
    from mazegen.shapes import Shapes
    shape = Shapes._shape_0()
    assert len(shape) == 5
    assert len(shape[0]) == 3


def test_maze_generator_orchestrator(tmp_path: Any) -> None:
    from mazegen.mazegenerator import MazeGenerator
    maze_file = tmp_path / "maze_out.txt"
    data = {
        "WIDTH": 20,
        "HEIGHT": 15,
        "ENTRY": (0, 0),
        "EXIT": (14, 19),
        "OUTPUT_FILE": str(maze_file),
        "PERFECT": True
    }
    mg = MazeGenerator(data)
    assert mg.valid is True
    assert maze_file.exists()


def test_data_validator_wide_maze() -> None:
    data = {
        "WIDTH": 30,
        "HEIGHT": 10,
        "ENTRY": (0, 29),
        "EXIT": (9, 0),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    validator = DataValidator(data)
    assert validator.valid is True
    assert validator.entry == (0, 29)
    assert validator.exit == (9, 0)
