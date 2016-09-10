import math
import numpy as np

def get_frequencies(sample, min, max, bins):
    frequencies = []

    interval = max - min
    binsize = interval / bins

    for x in range(0, bins):
        frequencies.append(0)

    for value in sample:
        x = math.floor(value / binsize)
        frequencies[x] += 1
    return frequencies


def chi_square(observed, expected):
    N = min(len(observed), len(expected))
    v = 0
    for n in range(0, N):
        v += ((observed[n] - expected[n]) ** 2) / expected[n]
    return v



