from  parsing import FileHandler
from tools import color_pallete as color
from tools import style_pallete as style
from tools import error_msg, info_msg, test_msg, success_msg, warning_msg

import sys


if __name__ == "__main__":

    if len(sys.argv) == 1:
        error_msg("No valid input was given")
    if len(sys.argv) > 2:
        warning_msg(f"More then one input was giving processing only processing the first argument -{sys.argv[1]}")
    else:
        success_msg(f"")

    