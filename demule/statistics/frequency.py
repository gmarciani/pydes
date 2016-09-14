import math.floor


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