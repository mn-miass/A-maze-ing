import sys
import os
import time
from typing import Optional
from styles import Color, Style
from parsing import Parsing
from mazegen import MazeGenerator
from display import DisplayMaze


def display_menu() -> None:
    print(f"{Color.BLUE}=========================================="
          f"{Style.RESET}")
    print(f"{Color.CYAN}{Style.BOLD}         🧩 MAZE ARCHITECT v1.0         "
          f"{Style.RESET}")
    print(f"{Color.BLUE}=========================================="
          f"{Style.RESET}")
    print(f"  {Color.WHITE}Construction & View:"
          f"{Style.RESET}")
    print(f"  {Color.BLUE}──────────────────────────────────────"
          f"{Style.RESET}")
    print(f"  {Color.CYAN}[1]{Style.RESET} 🔄 {Color.WHITE}Regenerate "
          f"Maze Layout{Style.RESET}")
    print(f"  {Color.CYAN}[2]{Style.RESET} 👁️  {Color.WHITE}Show/Hide "
          f"Solution Path{Style.RESET}")
    print(f"  {Color.CYAN}[3]{Style.RESET} 🎨 {Color.WHITE}Rotate or "
          f"Change Theme Colors{Style.RESET}")
    print(f"  {Color.CYAN}[4]{Style.RESET} 🔢 {Color.WHITE}Change "
          f"Numbers{Style.RESET}")
    print(f"  {Color.CYAN}[5]{Style.RESET} 🌈 {Color.WHITE}Toggle "
          f"Theme{Style.RESET}")
    print(f"\n  {Color.RED}[6]{Style.RESET} ❌ {Color.WHITE}Quit "
          f"Architect{Style.RESET}")
    print(f"  {Color.BLUE}──────────────────────────────────────"
          f"{Style.RESET}")
    print(f"  {Color.WHITE}Status: {Color.GREEN}READY{Color.WHITE} | "
          f"User: {Color.GREEN}ADMIN{Style.RESET}")
    print(f"{Color.BLUE}=========================================="
          f"{Style.RESET}")
    print(f"{Style.BOLD}{Color.YELLOW}>> Selection: "
          f"{Style.RESET}", end="")


def generate_maze(
    colors: dict[str, str],
    display_path: bool,
    display_info: bool,
    save_data: Optional[Parsing],
    save_maze: Optional[MazeGenerator],
) -> tuple[Parsing, MazeGenerator]:
    os.system("clear")
    if save_data is None:
        save_data = Parsing(sys.argv[1], display_info)

    data = save_data

    if data.config is None:
        raise RuntimeError("Parsing failed (config is None)")

    if display_info:
        input("Enter to continue...")

    os.system("clear")
    if save_maze is None:
        save_maze = MazeGenerator(data.config)
    maze = save_maze
    if maze.maze is None:
        raise RuntimeError("Maze generation failed (maze.maze is None)")

    DisplayMaze(
        maze.maze.grid_dec, maze.maze.grid_flags,
        data.config["ENTRY"], data.config["EXIT"],
        display_path,
        colors["Wall Color"], colors["Paths Color"], colors["Number Color"],
        colors["Entry Color"], colors["Exit Color"],
        colors["Border_Color"],
    )
    time.sleep(0.2)
    return (data, maze)


THEMES: list[dict[str, str]] = [
    {
        "Wall Color": Color.BG_BLACK,
        "Paths Color": Color.BG_WHITE,
        "Number Color": Color.BG_RED,
        "Entry Color": Color.BG_MAGENTA,
        "Exit Color": Color.BG_YELLOW,
        "Border_Color": Color.BG_BLUE,
    },
    {
        "Wall Color": Color.BG_BLUE,
        "Paths Color": Color.BG_CYAN,
        "Number Color": Color.BG_WHITE,
        "Entry Color": Color.BG_GREEN,
        "Exit Color": Color.BG_RED,
        "Border_Color": Color.BG_BLACK,
    },
    {
        "Wall Color": Color.BG_GREEN,
        "Paths Color": Color.BG_BLACK,
        "Number Color": Color.BG_YELLOW,
        "Entry Color": Color.BG_WHITE,
        "Exit Color": Color.BG_RED,
        "Border_Color": Color.BG_CYAN,
    },
    {
        "Wall Color": Color.BG_RED,
        "Paths Color": Color.BG_BLACK,
        "Number Color": Color.BG_YELLOW,
        "Entry Color": Color.BG_WHITE,
        "Exit Color": Color.BG_CYAN,
        "Border_Color": Color.BG_MAGENTA,
    },
    {
        "Wall Color": Color.BG_WHITE,
        "Paths Color": Color.BG_CYAN,
        "Number Color": Color.BG_BLUE,
        "Entry Color": Color.BG_GREEN,
        "Exit Color": Color.BG_MAGENTA,
        "Border_Color": Color.BG_BLACK,
    },
]


def toggle_theme(current_colors: dict[str, str], theme_index: int) -> int:
    """Toggle to the next theme and update current_colors in place.

    Args:
        current_colors: The active color dict to update.
        theme_index: The current theme index.

    Returns:
        The new theme index.
    """
    theme_index = (theme_index) % len(THEMES)
    current_colors.update(THEMES[theme_index])
    return theme_index


def change_colors(current_colors: dict[str, str]) -> None:
    color_options: dict[int, str] = {
        1: Color.BG_RED,
        2: Color.BG_BLUE,
        3: Color.BG_CYAN,
        4: Color.BG_YELLOW,
        5: Color.BG_MAGENTA,
        6: Color.BG_GREEN,
        7: Color.BG_WHITE,
        8: Color.BG_BLACK,
    }

    for item in current_colors:
        os.system("clear")
        print(f"1: {Color.BG_RED}   {Color.RESET}")
        print(f"2: {Color.BG_BLUE}   {Color.RESET}")
        print(f"3: {Color.BG_CYAN}   {Color.RESET}")
        print(f"4: {Color.BG_YELLOW}   {Color.RESET}")
        print(f"5: {Color.BG_MAGENTA}   {Color.RESET}")
        print(f"6: {Color.BG_GREEN}   {Color.RESET}")
        print(f"7: {Color.BG_WHITE}   {Color.RESET}")
        print(f"8: {Color.BG_BLACK}   {Color.RESET}")

        user_choice = input(f"{Style.BOLD}{Color.YELLOW}>> {item}: "
                            f"{Style.RESET}")

        if user_choice.isdigit() and int(user_choice) in color_options:
            current_colors[item] = color_options[int(user_choice)]
        else:
            print("Invalid input, skipping...")
            time.sleep(1)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            print(f"\n{Style.BOLD}{Color.CYAN}{'=' * 45}{Style.RESET}")
            print(f"{Style.BOLD}{Color.CYAN}  A-Maze-ing — Maze Generator"
                  f"{Style.RESET}")
            print(f"{Style.BOLD}{Color.CYAN}{'=' * 45}{Style.RESET}")
            print(f"  {Style.DIM}Usage:  {Style.RESET} "
                  "python3 a_maze_ing.py <config>")
            print(f"{Style.BOLD}{Color.CYAN}{'=' * 45}{Style.RESET}")
            print(f"  {Color.BG_RED}{Color.WHITE}{Style.BOLD} ERROR "
                  f"{Style.RESET} No configuration file provided.\n")
            sys.exit(1)

        active_colors: dict[str, str] = {
            "Wall Color": Color.BG_WHITE,
            "Paths Color": Color.BG_BLACK,
            "Number Color": Color.BG_RED,
            "Entry Color": Color.BG_MAGENTA,
            "Exit Color": Color.BG_YELLOW,
            "Border_Color": Color.BG_BLUE,
        }
        save_data, save_maze = generate_maze(
            active_colors,
            display_path=False,
            display_info=True,
            save_data=None,
            save_maze=None,
        )
        count_theme = 0
        display_path = False
        while True:
            display_menu()
            value_str = input()

            if not value_str.isdigit():
                os.system("clear")
                print("Wrong value was given")
                time.sleep(1)
                continue
            value = int(value_str)

            if value == 1:
                save_data, save_maze = generate_maze(
                    active_colors,
                    display_path,
                    display_info=False,
                    save_data=None,
                    save_maze=None,
                )
            elif value == 2:
                if display_path:
                    display_path = False
                else:
                    display_path = True

                save_data, save_maze = generate_maze(
                    active_colors,
                    display_path,
                    display_info=False,
                    save_data=save_data,
                    save_maze=save_maze,
                )
            elif value == 3:
                change_colors(active_colors)
                save_data, save_maze = generate_maze(
                    active_colors,
                    display_path,
                    display_info=False,
                    save_data=save_data,
                    save_maze=save_maze,
                )
            elif value == 4:
                os.system("clear")
                msg_str = input(
                    f"{Style.BOLD}{Color.YELLOW}"
                    f">> Enter the number(00 up to 99): {Style.RESET}"
                )
                if msg_str.isdigit():
                    msg_int = int(msg_str)
                    if 0 <= msg_int <= 99:
                        if save_data.config is not None:
                            save_data.config["MSG"] = msg_int
                save_data, save_maze = generate_maze(
                    active_colors,
                    display_path,
                    display_info=False,
                    save_data=save_data,
                    save_maze=None,
                )
            elif value == 5:
                theme = toggle_theme(active_colors, count_theme)
                active_colors = THEMES[theme]
                save_data, save_maze = generate_maze(
                    active_colors,
                    display_path,
                    display_info=False,
                    save_data=save_data,
                    save_maze=None,
                )
                count_theme += 1
            elif value == 6:
                os.system("clear")
                print("exiting the program....")
                break
            else:
                os.system("clear")
                print("Wrong value was given")
    except BaseException as e:
        print(e)
