import math

from controls.plots.randomness_plots import ks_histogram
from libs.des.rvms import cdfChisquare


def ksdistances(statistics, bins):
    statistics.sort()
    k = len(statistics)
    distances = []
    for i in range(k):
        chi = statistics[i]
        distance = abs(cdfChisquare(bins - 1, chi) - (i / k))
        distances.append((chi, distance))
    return distances


def ksstatistic(distances):
    return max(value[1] for value in distances)


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


def plot(distances, mx):
    title = 'Test of Kolmogorov-Smirnov'
    figure = ks_histogram(title, distances, mx)
    return figure