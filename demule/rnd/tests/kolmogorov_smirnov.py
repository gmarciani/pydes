import math
from libs.des.rvms import cdfChisquare
from plots.kolmogorov_smirnov import histogram as kshistogram


def ksdistances(chisquares, bins):
    chisquares.sort()
    streams = len(chisquares)
    distances = []
    for i in range(streams):
        chi = chisquares[i]
        distance = abs(cdfChisquare(bins - 1, chi) - (i / streams))
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


def plot(title, ksdistances, kspoint, kscritical):
    figure = kshistogram(title, ksdistances, kspoint, kscritical)
    return figure