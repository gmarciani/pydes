import math
from statistics.chisquare import chisquare_bivariate
from libs.des.rvms import idfChisquare
from plots.chisquare import scatter as chisquare_scatter


# hint: samsize >= 10*(bins^2), bins >= 100, confidence = 0.95


def observations(uniform, samsize, bins):
    observed = [[0 for _ in range(bins)] for _ in range(bins)]

    for value in range(samsize):
        u1 = uniform()
        u2 = uniform()
        b1 = math.floor(u1 * bins)
        b2 = math.floor(u2 * bins)
        observed[b1][b2] += 1

    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x1, x2: samsize / (bins ** 2)
    value = chisquare_bivariate(observed, expected)
    return value


def critical_min(bins, confidence):
    return idfChisquare((bins ** 2) - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare((bins ** 2) - 1, 1 - (1 - confidence) / 2)


def plot(title, data, min, max):
    figure = chisquare_scatter(title, data, min, max)
    return figure