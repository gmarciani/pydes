import math
import numpy as np


def get_frequencies(sample, min, max, bins):
    frequencies = []

    interval = max - min
    binsize = interval / bins

    for bin in range(0, bins):
        frequencies.append(0)

    for value in sample:
        bin = math.floor(value / binsize)
        frequencies[bin] += 1

    return frequencies


def get_frequencies_bivariate(sample, min, max, bins):
    frequencies = []

    interval = max -min
    binsize = interval / bins

    for bin1 in range(0, bins):
        frequencies.append([])
        for bin2 in range(0, bins):
            frequencies[bin1].append(0)

    for values in sample:
        bin1 = math.floor(values[0] / binsize)
        bin2 = math.floor(values[1] / binsize)
        frequencies[bin1][bin2] += 1

    return frequencies


def chi_square(observed, expected):
    N = min(len(observed), len(expected))
    v = 0
    for n in range(0, N):
        v += ((observed[n] - expected[n]) ** 2) / expected[n]
    return v



