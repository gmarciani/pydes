import math
from libs.des.rvms import idfChisquare
from controls.statistics import get_frequencies

def test(sample, bins, confidence): # hint: bins >= 1000, len(sample) >= 10bins, confidence=0.95
    report = {}

    report['chi-square'] = chisquare_from_sample(sample, bins)
    report['critical-min'] = critical_min(bins, confidence)
    report['critical-max'] = critical_max(bins, confidence)

    return report


def chisquare_from_sample(sample, bins):
    frequencies = get_frequencies(sample, 0, 1, bins)
    N = len(frequencies)
    expected = len(sample) / N
    v = 0
    for n in range(0, N):
        v += ((frequencies[n] - expected) ** 2) / expected
    return v


def chisquare(observed, samplesize):
    N = len(observed)
    expected = samplesize / N
    v = 0
    for n in range(0, N):
        v += ((observed[n] - expected) ** 2) / expected
    return v


def critical_min(bins, confidence):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)