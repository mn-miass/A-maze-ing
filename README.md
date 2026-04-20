*This project has been created as part of the 42 curriculum by mn-miass, hadrider.*

---

## Description

A-Maze-ing is a terminal-based maze generator written in Python 3. It reads a configuration file, generates a maze using the **Hunt-and-Kill** algorithm, and displays it in the terminal with full ANSI colour support. The maze always embeds a visible **"42" pattern** made of fully-walled cells, and can optionally be **perfect** (exactly one path between entry and exit). The solution path is computed via BFS and written to the output file alongside the maze grid in hexadecimal format.

Key features:
- Perfect or imperfect maze generation with optional seed for reproducibility
- BFS shortest-path solver with direction string output (N/E/S/W)
- Interactive terminal UI: regenerate, toggle solution path, change colours, cycle themes
- Reusable `mazegen` package installable via pip
- Full config-file validation with clear error reporting and optional log file


---

## Instructions

### Requirements

- Python 3.12 or later
- pip

### Install dependencies

```bash
make install
```

### Run

```bash
make run                        # uses default config.txt
python3 a_maze_ing.py config.txt  # explicit config file
```

### Debug

```bash
make debug
```

### Lint

```bash
make lint          # flake8 + mypy standard
make lint-strict   # flake8 + mypy --strict
```

### Clean

```bash
make clean
```

---

## Configuration File Format

The config file contains one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored. Inline comments (after `#`) are also supported.

### Mandatory keys

| Key           | Type        | Constraints                        | Example                  |
|---------------|-------------|------------------------------------|--------------------------|
| `WIDTH`       | integer     | >= 9                               | `WIDTH=20`               |
| `HEIGHT`      | integer     | >= 7                               | `HEIGHT=15`              |
| `ENTRY`       | `row,col`   | non-negative, within maze bounds   | `ENTRY=0,0`              |
| `EXIT`        | `row,col`   | non-negative, within maze bounds, ≠ ENTRY | `EXIT=14,19`    |
| `OUTPUT_FILE` | string      | must be writable path              | `OUTPUT_FILE=maze.txt`   |
| `PERFECT`     | bool        | `true`/`false`/`1`/`0`            | `PERFECT=True`           |

### Optional keys

| Key         | Type    | Constraints             | Default    | Example            |
|-------------|---------|-------------------------|------------|--------------------|
| `SEED`      | integer | any integer             | random     | `SEED=42`          |
| `LOG_FILE`  | string  | writable, ≠ OUTPUT_FILE | none       | `LOG_FILE=log.txt` |
| `MSG`       | integer | 0–99                    | `42`       | `MSG=42`           |

### Example `config.txt`

```ini
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=14,19
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
MSG=42
# LOG_FILE=log.txt
```

---

## Output File Format

Each row of the maze is written as a sequence of hexadecimal digits (one per cell), one row per line. Each hex digit encodes which walls are **closed** using a 4-bit bitmask:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1       | East  |
| 2       | South |
| 3       | West  |

A set bit means the wall is **closed**; a clear bit means it is **open**.

After an empty line, three additional lines follow:
1. Entry coordinates: `row,col`
2. Exit coordinates: `row,col`
3. Shortest path as a direction string using `N`, `E`, `S`, `W`

Example:
```
9F3A...
...
1,1
19,14
SWSESWSE...ENEE
```

---

## Maze Generation Algorithm

This project uses the **Hunt-and-Kill** algorithm.

### How it works

1. Start at cell (0, 0) and mark it as visited.
2. **Kill phase** — randomly walk to an unvisited neighbour, carve a passage, mark it visited. Repeat until stuck.
3. **Hunt phase** — scan the grid row by row to find an unvisited cell that has at least one visited neighbour. Carve a passage from that neighbour into the unvisited cell and resume the kill phase from there.
4. Repeat until all reachable cells are visited.

### Why Hunt-and-Kill?

- Produces **long, winding corridors** with relatively few dead ends — visually interesting mazes.
- Simple to implement with no external data structures (no stack, no union-find).
- Naturally supports a **seed** for reproducibility.
- Works well alongside the pre-set "42" pattern cells (which are simply skipped as unvisited and uncarveable).

When `PERFECT=False`, a post-processing pass randomly removes additional walls to create loops and multiple paths.

---

## Reusable Module — `mazegen`

The `mazegen` package is the standalone, reusable part of this project. It handles everything from input validation to maze generation and pathfinding, with no dependency on the display or parsing modules.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```


### Basic usage

```python
from mazegen import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (14, 19),
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": True,
}

maze = MazeGenerator(config)

if maze.valid:
    # Access the decimal wall grid (2D list of ints, 0–15)
    grid = maze.maze.grid_dec

    # Access the hex grid (2D list of single hex chars)
    hex_grid = maze.maze.grid_hex

    # Access the solution path as a direction string
    path_str = maze.path.direction   # e.g. "SSEENWW..."

    # Access the solution path as a list of (row, col) tuples
    path_coords = maze.path.path
```

### Custom parameters

```python
config = {
    "WIDTH": 30,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (19, 29),
    "OUTPUT_FILE": "out.txt",
    "PERFECT": False,
    "SEED": 1337,   # optional — omit for random
    "MSG": 99,      # optional — two-digit number to embed (default 42)
}
maze = MazeGenerator(config)
```

## Interactive Controls

Once the maze is displayed, the menu offers:

| Key | Action |
|-----|--------|
| `1` | Regenerate a new maze (new random seed) |
| `2` | Toggle the solution path overlay |
| `3` | Manually set each colour slot |
| `4` | Change the embedded number (0–99) |
| `5` | Cycle through preset colour themes |
| `6` | Quit |

---

## Team & Project Management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| `mn-miass` | *e.g. maze generation algorithm, parsing, reusable package* |
| `hadrider` | *e.g. pathfinder, display, interactive menu* |

### Planning

*Describe your initial timeline and how it evolved here.*

### What worked well

*e.g. separating parsing and generation cleanly made testing easy.*

### What could be improved

*e.g. the display module's import of `styles` is fragile and should use proper relative imports.*

### Tools used

- Python 3.10+
- flake8, mypy (linting and type checking)
- pytest (unit testing)


---

## Resources

- [Maze generation visualizer](hhttps://dqwertyc.github.io/unity-maze-generator/)
- [Hunt and kill explenation](https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm)
- [Breadth-First Search](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/)


### AI usage

Claude AI was used for:
- Explaining new concepts (hex wall encoding, BFS pathfinding)
- helping with the READme file