from tests.rnd.randomness import uniformity_univariate
from tests.rnd.randomness import uniformity_bivariate
from tests.rnd.randomness import extremes
from tests.rnd.randomness import runsup
from tests.rnd.randomness import gap
from tests.rnd.randomness import permutation


def _test():
    uniformity_univariate.test()
    uniformity_bivariate.test()
    extremes.test()
    runsup.test()
    gap.test()
    permutation.test()


if __name__ == '__main__':
    _test()

