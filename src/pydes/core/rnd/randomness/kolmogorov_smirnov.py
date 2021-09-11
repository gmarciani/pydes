"""
Kolmogorov-Smirnov test of randomness.
"""
import math

from pydes.core.rnd.rndf import cdfChisquare

# Approximation table for one-tailed critical values by Stephens.
C_FACTOR_TABLE = {"0.900": 1.224, "0.950": 1.358, "0.975": 1.480, "0.990": 1.628}


def compute_ks_distances(chisquares, bins):
    """
    Compute the Kolmogorov-Smirnov distances for all Chi-Square statistics.
    :param chisquares: the Chi-Sqaure statistics for all streams.
    :param bins: the number of bins.
    :return: the Kolmogorov-Smirnov distances for all Chi-Square statistics.
    """
    chisquares.sort(key=lambda v: v[1])
    streams = len(chisquares)
    ks_distances = []
    for i in range(streams):
        chi = chisquares[i][1]
        ks_distance = _compute_ks_distance(chi, i, streams, bins)
        ks_distances.append((chi, ks_distance))
    return ks_distances


def _compute_ks_distance(chi, i, streams, bins):
    """
    Compute the Kolmogorov-Smirnov distance for a stream.
    :param chi: the Chi-Square statistic.
    :param i: the stream number.
    :param streams: the total number of streams.
    :param bins: the number of bins.
    :return: the Kolmogorov-Smirnov distance for a stream.
    """
    theoreticalCdf = cdfChisquare(bins - 1, chi)
    return max(abs(theoreticalCdf - (i / streams)), abs(theoreticalCdf - ((i - 1) / streams)))


def compute_ks_statistic(ks_distances):
    """
    Compute the Kolmogorov-Smirnov statistic for the given Kolmogorov-Smirnov distances.
    :param ks_distances: the Kolmogorov-Smirnov distances.
    :return: the Kolmogorov-Smirnov statistic for the given Kolmogorov-Smirnov distances.
    """
    return max(value[1] for value in ks_distances)


def compute_ks_point(ks_distances):
    """
    Compute the Kolmogorov-Smirnov point for the given Kolmogorov-Smirnov distances.
    :param ks_distances: the Kolmogorov-Smirnov distances.
    :return: the Kolmogorov-Smirnov point for the given Kolmogorov-Smirnov distances.
    """
    return max(ks_distances, key=lambda value: value[1])[0]


def compute_ks_critical_distance(n, confidence):
    """
    Compute the one-tailed critical value of KS distance, leveraging the Stephens approximation.
    :param n: the sample size (number of streams).
    :param confidence: the confidence level, must be one of [0.90,0.95,0.975,0.99].
    :return: the one-tailed critical value of KS distance.
    """
    return C_FACTOR_TABLE[format(confidence, ".3f")] / (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n))
