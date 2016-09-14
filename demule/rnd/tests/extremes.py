import math

from statistics.chisquare import chisquare_univariate
from libs.des.rvms import idfChisquare
from plots.chisquare import scatter as chisquare_scatter


# hint: samsize >= 10*bins, bins >= 1000, d >= 2, confidence = 0.95


def observations(uniform, samsize, bins, d):
    observed = [0] * bins

    for _ in range(samsize):
        u1 = uniform()
        for _ in range(1, d):
            u2 = uniform()
            if u2 > u1:
                u1 = u2
        u = u1 ** d
        b = math.floor(u * bins)
        observed[b] += 1

    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = chisquare_univariate(observed, expected)
    return value

def critical_min(bins, confidence):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def plot(title, data, min, max):
    figure = chisquare_scatter(title, data, min, max)
    return figure