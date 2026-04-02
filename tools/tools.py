import time
import sys
from .style import color_pallete as color
from .style import style_pallete as style

def display_msg(msg, sec, out=sys.stdout):
    for letter in msg:
        print(letter, end="", flush=True, file=out) 
        time.sleep(sec)
    print()


def error_msg(msg, sec=0.001, file=sys.stderr):
    msg = f"{color.AMEDINA}{style.BOLD}[ERROR]   :" + msg
    display_msg(msg, sec, file)


def test_msg(msg, sec=0, file=sys.stdout):
    msg = f"{color.GRAY}{style.BOLD}[TEST]    :{color.RESET}" + msg + "......"
    display_msg(msg, sec, file)


def warning_msg(msg, sec=0, file=sys.stdout):
    msg = f"{color.ORANGE}{style.BOLD}[WARNING] :{color.RESET}" + msg
    display_msg(msg, sec, file)


def success_msg(msg, sec=0.001, file=sys.stdout):
    msg = f"{color.GREEN}{style.BOLD}[SUCCESS] :{color.RESET}" + msg
    display_msg(msg, sec, file)


def info_msg(msg, sec=0.001, file=sys.stdout):
    msg = f"{color.MAHDI}{style.BOLD}[INFO]    :{color.RESET}" + msg
    display_msg(msg, sec, file)
