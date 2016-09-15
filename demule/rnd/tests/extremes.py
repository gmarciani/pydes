import math
from statistics.chisquare import chisquare_univariate
from libs.des.rvms import idfChisquare
from rnd.tests.error import error_two_tails
from plots.chisquare import scatter


SAMSIZE = 10000     # SAMSIZE >= 10*BINS
BINS = 1000         # BINS >= 1000
D = 5               # D >= 2
CONFIDENCE = 0.95   # CONFIDENCE >= 0.95


def statistics(generator, streams, samsize=SAMSIZE, bins=BINS, d=D):
    data = []
    for stream in range(streams):
        generator.stream(stream)
        observed = observations(generator.rnd, samsize, bins, d)
        chi = chisquare(observed, samsize)
        result = (stream, chi)
        data.append(result)
    return data


def observations(uniform, samsize, bins, d):
    observed = [0] * bins
    for _ in range(samsize):
        u1 = uniform()
        for _ in range(1, d):
            u2 = uniform()
            if u2 > u1:
                u1 = u2
        u = u1 ** d
        b = math.floor(u * bins)
        observed[b] += 1
    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)