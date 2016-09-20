"""
Experiment: Kolmogorov-Smirnov test on all Chi-Square tests.
"""

from tests.experiments.randomness import kolmogorov_smirnov


def experiment():
    kolmogorov_smirnov.test('uniformity_univariate', dict(samsize=10000, bins=1000, confidence=0.95))
    kolmogorov_smirnov.test('uniformity_bivariate', dict(samsize=100000, bins=100, confidence=0.95))
    kolmogorov_smirnov.test('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5))
    kolmogorov_smirnov.test('runsup', dict(samsize=14400, bins=6, confidence=0.95))
    kolmogorov_smirnov.test('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99))
    kolmogorov_smirnov.test('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))


if __name__ == '__main__':
    experiment()

