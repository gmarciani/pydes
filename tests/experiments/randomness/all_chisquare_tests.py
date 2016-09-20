"""
Experiment: All Chi-Square Tests of Randomness.
"""

from tests.experiments.randomness import uniformity_univariate
from tests.experiments.randomness import uniformity_bivariate
from tests.experiments.randomness import extremes
from tests.experiments.randomness import runsup
from tests.experiments.randomness import gap
from tests.experiments.randomness import permutation


def experiment():
    uniformity_univariate.experiment()
    uniformity_bivariate.experiment()
    extremes.experiment()
    runsup.experiment()
    gap.experiment()
    permutation.experiment()


if __name__ == '__main__':
    experiment()

