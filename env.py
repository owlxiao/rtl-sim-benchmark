import os
import subprocess

from shutil import which
from pathlib import Path


def color_print(color, name, message):
    # This uses ANSI escape codes to set text color
    colors = {
        'red': 1,
        'green': 2,
        'yellow': 3,
        'blue': 4,
        'white': 7
    }
    print(f"\033[3{colors[color]}m{name}\t\033[3{colors['white']}m{message}")


def show_status(tool_name):
    tool_path = which(tool_name)

    if tool_path is None:
        color_print('red', tool_name, "is not found")
        return False
    else:
        color_print('green', tool_name, f"is at {tool_path}")
        return True


def show_status_all():
    print("Check Tools")
    tools = ["verilator", "arcilator", "firtool", "clang++"]

    for tool in tools:
        show_status(tool)


if __name__ == "__main__":
    show_status_all()
