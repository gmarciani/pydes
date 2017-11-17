"""
The Gap Test for independence.
"""

from demule.utils import rvms
from demule.utils import errutils
from demule.utils import mathutils
from demule.plots.chisquare import scatter


SAMSIZE = 10000     # SAMSIZE >= 10000
BINS = 78           # BINS <= 2+floor(ln(10/samsize*(b-a))/(ln(1-b+a)))
A = 0.94            # 0 <= a < b <= 1
B = 0.99            # 0 <= a < b <= 1
CONFIDENCE = 0.95   # CONFIDENCE >= 0.95


def statistics(generator, streams, samsize=SAMSIZE, bins=BINS, a=A, b=B):
    data = []
    for stream in range(streams):
        generator.stream(stream)
        observed = observations(generator.rnd, samsize, bins, a, b)
        chi = chisquare(observed, samsize, a, b)
        result = (stream, chi)
        data.append(result)
    return data


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
    value = mathutils.chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return rvms.idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return rvms.idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return errutils.error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)