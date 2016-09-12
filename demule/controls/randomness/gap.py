from controls.plots.randomness_plots import scatter
from controls.statistics import chisquare_univariate
from libs.des.rvms import idfChisquare


# hint: samsize >= 10000, bins <= 2+floor(ln(10/samsize*(b-a))/(ln(1-b+a))), 0 <= a < b <= 1, confidence = 0.95,


def observations(uniform, samsize, bins, a, b):
    observed = [0] * bins

    for _ in range(samsize):
        b = 0
        u = uniform()
        while u <= a or u >= b:
            b += 1
            u = uniform()
        if b > bins - 1:
            b = bins - 1
        observed[b] += 1

    return observed


def chisquare(observed, samsize, a, b):
    bins = len(observed)
    expected = lambda x: samsize * ((1 - b + a) ** (bins - 1)) if (x == bins -1) else samsize * (b - a) * ((1 - b + a) ** x)
    value = chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def plot(data, min, max):
    title = 'Test of Independence (Gap)'
    figure = scatter(title, data, min, max)
    return figure