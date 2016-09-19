"""
The Test of Runs-Up for independence.
"""

import math

from demule.utils import mathutils
from libs.des.rvms import idfChisquare
from plots.chisquare import scatter
from utils.error import error_two_tails

SAMSIZE = 14400     # SAMSIZE >= 7200
BINS = 6            # BINS >= 6
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
    expected = lambda x: samsize * x / math.factorial(x + 1)
    value = mathutils.chisquare_univariate(observed, expected, start=1)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)