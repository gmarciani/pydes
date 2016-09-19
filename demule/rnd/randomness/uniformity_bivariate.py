"""
The Test of Bivariate Uniformity for uniformity.
"""

import math

from demule.utils import mathutils
from libs.des.rvms import idfChisquare
from plots.chisquare import scatter
from utils.error import error_two_tails

SAMSIZE = 10000     # SAMSIZE >= 10*(BINS^2)
BINS = 1000         # BINS >= 100
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
    observed = [[0 for _ in range(bins)] for _ in range(bins)]
    for value in range(samsize):
        u1 = uniform()
        u2 = uniform()
        b1 = math.floor(u1 * bins)
        b2 = math.floor(u2 * bins)
        observed[b1][b2] += 1
    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x1, x2: samsize / (bins ** 2)
    value = mathutils.chisquare_bivariate(observed, expected)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return idfChisquare((bins ** 2) - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return idfChisquare((bins ** 2) - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)