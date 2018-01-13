"""
Spectral Test

# Zoom interval
DEFAULT_INTERVAL = (0.0, 1.0)
"""

from core.utils.file_utils import save_list_of_pairs, append_list_of_pairs

# Number of observations in memory before flushing into file
MAX_OBSERVATIONS_BEFORE_FLUSH = 10


def statistics(filename, rndgen, samsize, interval):
    low = interval[0]
    high = interval[1]

    observed = []
    found = 0
    save_list_of_pairs(filename, observed)

    u1 = rndgen.rnd()
    for i in range(1, samsize):
        u2 = rndgen.rnd()
        if low <= u1 <= high and low <= u2 <= high:
            found += 1
            observed.append((u1, u2))
            print("Found: {} | {}/{}".format(found, i, samsize))
        u1 = u2
        if len(observed) == MAX_OBSERVATIONS_BEFORE_FLUSH:
            append_list_of_pairs(filename, observed)
            del observed[:]
    if len(observed) != 0:
        append_list_of_pairs(filename, observed)