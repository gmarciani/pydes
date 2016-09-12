import math

from controls.plots.randomness_plots import scatter
from controls.statistics import chisquare_univariate
from libs.des.rvms import idfChisquare


# hint: samsize >= 7200, bins = 6, confidence = 0.95


def observations(uniform, samsize, bins):
    observed = [0] * (bins + 1)

    for _ in range(samsize):
        b = 1
        u = uniform()
        t = uniform()
        while t > u:
            b += 1
            u = t
            t = uniform()
        if b > bins:
            b = bins
        observed[b] += 1

    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize * x / math.factorial(x + 1)
    value = chisquare_univariate(observed, expected, start=1)
    return value


def critical_min(bins, confidence):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def plot(data, min, max):
    title = 'Test of Independence (Runs-Up)'
    figure = scatter(title, data, min, max)
    return figure