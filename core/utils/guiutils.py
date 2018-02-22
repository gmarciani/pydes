"""
Utilities for CLI.
"""


import sys


def print_progress(iteration, total, prefix="Progress", suffix="Complete", decimals=0, bar_length=50):
    format_string = "{0:." + str(decimals) + "f}"
    percents = format_string.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "=" * filled_length + " " * (bar_length - filled_length)

    sys.stdout.flush()

    sys.stdout.write("\r%s [%s] %s%s %s" % (prefix, bar, percents, "%", suffix))
    if iteration == total:
        sys.stdout.write("\n")


if __name__ == "__main__":
    from time import sleep

    for i in range(10):
        sleep(1)
        print_progress(i+1, 10)