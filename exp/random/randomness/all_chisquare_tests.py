"""
Experiment: All Chi-Square Tests of Randomness.
"""

from exp.random.randomness import extremes
from exp.random.randomness import gap
from exp.random.randomness import permutation
from exp.random.randomness import runsup
from exp.random.randomness import uniformity_bivariate
from exp.random.randomness import uniformity_univariate


def experiment():
    uniformity_univariate.experiment()
    uniformity_bivariate.experiment()
    extremes.experiment()
    runsup.experiment()
    gap.experiment()
    permutation.experiment()


if __name__ == '__main__':
    experiment()

