import math


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


def chisquare_univariate(observed, expected):
    K = len(observed)
    value = 0
    for x in range(0, K):
        value += ((observed[x] - expected) ** 2) / expected
    return value


def chisquare_bivariate(observed, expected):
    K = len(observed)
    value = 0
    for x1 in range(0, K):
        for x2 in range(0, K):
            value += ((observed[x1][x2] - expected) ** 2) / expected
    return value



