"""
Experiment: Kolmogorov-Smirnov test on all Chi-Square tests.
"""

from randomness import kolmogorov_smirnov as test
from core.rnd.rndgen import MarcianiMultiStream as RandomGenerator


def experiment():
    chisquare_tests = [
        ('uniformity_u', dict(samsize=10000, bins=1000, confidence=0.95)),
        ('uniformity_b', dict(samsize=100000, bins=100, confidence=0.95)),
        ('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5)),
        ('runsup', dict(samsize=14400, bins=6, confidence=0.95)),
        ('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99)),
        ('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))
    ]

    for t in chisquare_tests:
        test.experiment(RandomGenerator(), t[0], t[1])


if __name__ == '__main__':
    experiment()

