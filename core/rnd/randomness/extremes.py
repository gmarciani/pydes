"""
The Test of Extremes for uniformity.

SAMSIZE = 10000     # SAMSIZE >= 10*BINS
BINS = 1000         # BINS >= 1000
D = 5               # D >= 2
CONFIDENCE = 0.95   # CONFIDENCE >= 0.95
"""
import math
from core.rnd.rndf import idfChisquare
from core.utils import errutils
from core.utils import mathutils
from core.utils.guiutils import print_progress


def statistics(generator, samsize, bins, d):
    data = []
    streams = generator.get_nstreams()
    for stream in range(streams):
        generator.stream(stream)
        observed = observations(generator, samsize, bins, d)
        chi = _compute_chisquare_statistic(observed, samsize)
        result = (stream, chi)
        data.append(result)
        print_progress(stream, streams)
    return data


def observations(generator, samsize, bins, d):
    observed = [0] * bins
    for _ in range(samsize):
        u1 = generator.rnd()
        for _ in range(1, d):
            u2 = generator.rnd()
            if u2 > u1:
                u1 = u2
        u = u1 ** d
        b = math.floor(u * bins)
        observed[int(b)] += 1
    return observed


def _compute_chisquare_statistic(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = mathutils.chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence):
    """
    Compute the two-tailed critical min value.
    :param bins: the nuber of bins.
    :param confidence: the confidence level.
    :return: the two-tailed critical min value.
    """
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    """
    Compute the two-tailed critical max value.
    :param bins: the nuber of bins.
    :param confidence: the confidence level.
    :return: the two-tailed critical max value.
    """
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence):
    """
    Compute the error components.
    :param data: the collected data.
    :param mx: the critical value
    :param confidence: the confidence level.
    :return: (Dict) the dictionary of errors.
    """
    return errutils.error_two_tails(data, mn, mx, confidence)