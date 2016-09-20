"""
Kolmogorov-Smirnov test of randomness.
"""

import math
from demule.utils import rvms
from demule.utils import errutils
from demule.plots.kolmogorov_smirnov import histogram as kshistogram
from demule.plots.kolmogorov_smirnov import histogram2 as kshistogram2


CONFIDENCE = 0.95


def ksdistances(chisquares, bins):
    chisquares.sort(key=lambda v: v[1])
    streams = len(chisquares)
    distances = []
    for i in range(streams):
        chi = chisquares[i][1]
        distance = max(abs(rvms.cdfChisquare(bins - 1, chi) - (i / streams)), abs(rvms.cdfChisquare(bins - 1, chi) - ((i - 1) / streams)))
        distances.append((chi, distance))
    return distances


def kspoint(distances):
    return max(distances, key=lambda value: value[1])


def ksstatistic(distances):
    return max(value[1] for value in distances)


def critical_ksdistance(streams, confidence):
    c = c_factor(confidence)
    return c / (math.sqrt(streams) + 0.12 + 0.11 / math.sqrt(streams))


C_FACTOR_TABLE = {
    '0.900': 1.224,
    '0.950': 1.358,
    '0.975': 1.480,
    '0.990': 1.628
}


def c_factor(confidence):
    return C_FACTOR_TABLE[format(confidence, '.3f')]

def error(data, mx, confidence):
    return errutils.error_one_tail(data, mx, confidence)


def plot(ksdistances, kspoint, kscritical, title=None, filename=None):
    kshistogram(ksdistances, kspoint, kscritical, title, filename)


def plot2(chisquares, bins, kspoint, title=None, filename=None):
    kshistogram2(chisquares, bins, kspoint, title, filename)