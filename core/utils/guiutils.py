"""
Utilities for CLI.
"""

import sys
from core.utils.logutils import get_logger


logger = get_logger(__name__)


def print_progress(iteration, total, prefix="PROGRESS", suffix="Complete", message="", decimals=0, bar_length=50):
    format_string = "{0:." + str(decimals) + "f}"
    percents = format_string.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "=" * filled_length + " " * (bar_length - filled_length)

    sys.stdout.flush()

    sys.stdout.write("\r%s [%s] %s%s %s { %s }" % (prefix, bar, percents, "%", suffix, message))


if __name__ == "__main__":
    from time import sleep

    tot = 1000

    logger.info("Start")

    for i in range(tot+100):
        sleep(0.1/tot)
        print_progress(i+1, tot)

    logger.info("End")