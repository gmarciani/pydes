"""
Experiment: All Chi-Square Tests of Randomness.
"""

from experiments.randomness import extremes
from experiments.randomness import gap
from experiments.randomness import permutation
from experiments.randomness import runsup
from experiments.randomness import uniformity_bivariate
from experiments.randomness import uniformity_univariate


def experiment():
    uniformity_univariate.experiment()
    uniformity_bivariate.experiment()
    extremes.experiment()
    runsup.experiment()
    gap.experiment()
    permutation.experiment()


if __name__ == '__main__':
    experiment()

