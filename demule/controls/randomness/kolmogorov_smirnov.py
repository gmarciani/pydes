import math

from controls.plots.randomness_plots import scatter
from libs.des.rvms import cdfChisquare


def ksdistances(statistics):
    statistics.sort()
    k = len(statistics)
    fn = lambda x, i: sum(xi <= x for xi in statistics[:i]) / k
    distances = []
    for i in range(k):
        chi = statistics[i]
        distance = math.abs(cdfChisquare(k, chi) - fn(chi, i))
        distances.append((chi, distance))
    return distances


def critical_ksdistance(samsize, confidence):
    c = c_factor(confidence)
    return c / (math.sqrt(samsize) + 0.12 + 0.11 / math.sqrt(samsize))


C_FACTOR_TABLE = {
    '0.900': 1.224,
    '0.950': 1.358,
    '0.975': 1.480,
    '0.990': 1.628
}


def c_factor(confidence):
    return C_FACTOR_TABLE[format(confidence, '.3f')]


def plot(data, min, max):
    title = 'Test of Kolmogorov-Smirnov'
    figure = scatter(title, data, min, max)
    return figure