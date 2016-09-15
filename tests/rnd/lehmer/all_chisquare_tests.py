import unittest
from tests.rnd.lehmer import uniformity_univariate
from tests.rnd.lehmer import uniformity_bivariate
from tests.rnd.lehmer import extremes
from tests.rnd.lehmer import runsup
from tests.rnd.lehmer import gap
from tests.rnd.lehmer import permutation


uniformity_univariate.test()

uniformity_bivariate.test()

extremes.test()

runsup.test()

gap.test()

permutation.test()

