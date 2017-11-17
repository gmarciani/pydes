"""
The Test of Univariate Uniformity for uniformity.
"""

import math
from demule.utils.rvms import idfChisquare
from demule.utils import errutils
from demule.utils import mathutils
from demule.plots.chisquare import scatter


SAMSIZE = 10000     # SAMSIZE >= 10*BINS
BINS = 1000         # BINS >= 1000
CONFIDENCE = 0.95   # CONFIDENCE >= 0.95


def statistics(generator, streams, samsize=SAMSIZE, bins=BINS):
    data = []
    for stream in range(streams):
        generator.stream(stream)
        observed = observations(generator.rnd, samsize, bins)
        chi = chisquare(observed, samsize)
        result = (stream, chi)
        data.append(result)
    return data


def observations(uniform, samsize, bins):
    observed = [0] * bins
    for _ in range(samsize):
        u = uniform()
        b = math.floor(u * bins)
        observed[b] += 1
    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = mathutils.chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return errutils.error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)
