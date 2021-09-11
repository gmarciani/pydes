"""
Spectral Test

# Zoom interval
DEFAULT_INTERVAL = (0.0, 1.0)
"""
from core.utils.guiutils import print_progress
from core.utils.file_utils import empty_file
from core.utils.csv_utils import save_csv

# Number of observations in memory before flushing into file
MAX_OBSERVATIONS_BEFORE_FLUSH = 10


def statistics(filename, rndgen, samsize, interval):
    empty_file(filename)

    header = ["u1", "u2"]

    low = interval[0]
    high = interval[1]

    observed = []
    found = 0

    u1 = rndgen.rnd()
    for i in range(1, samsize):
        u2 = rndgen.rnd()
        if low <= u1 <= high and low <= u2 <= high:
            found += 1
            observed.append((u1, u2))
            print_progress(i, samsize, message="Found {}".format(found))
        u1 = u2

        if len(observed) == MAX_OBSERVATIONS_BEFORE_FLUSH:
            save_csv(filename, header, observed, append=True)
            del observed[:]
    if len(observed) != 0:
        save_csv(filename, header, observed, append=True)
