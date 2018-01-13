"""
Experiment: All Chi-Square Tests of Randomness.
"""

from experiments.random.randomness import extremes
from experiments.random.randomness import gap
from experiments.random.randomness import permutation
from experiments.random.randomness import runsup
from experiments.random.randomness import uniformity_bivariate
from experiments.random.randomness import uniformity_univariate


def experiment():
    uniformity_univariate.experiment()
    uniformity_bivariate.experiment()
    extremes.experiment()
    runsup.experiment()
    gap.experiment()
    permutation.experiment()


if __name__ == '__main__':
    experiment()

