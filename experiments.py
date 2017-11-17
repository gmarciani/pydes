import os
import sys

sys.path.append(os.path.abspath('.'))

from experiments.inspection import modulus
from experiments.inspection import multipliers
from experiments.inspection import jumpers
from experiments.randomness import uniformity_univariate
from experiments.randomness import uniformity_bivariate
from experiments.randomness import extremes
from experiments.randomness import runsup
from experiments.randomness import gap
from experiments.randomness import permutation
from experiments.randomness import kolmogorov_smirnov
from experiments.randomness import spectral

modulus.experiment()
multipliers.experiment()
jumpers.experiment()

spectral.experiment()

uniformity_univariate.experiment()
uniformity_bivariate.experiment()
extremes.experiment()
runsup.experiment()
gap.experiment()
permutation.experiment()

kolmogorov_smirnov.test('uniformity_univariate', dict(samsize=10000, bins=1000, confidence=0.95))
kolmogorov_smirnov.test('uniformity_bivariate', dict(samsize=100000, bins=100, confidence=0.95))
kolmogorov_smirnov.test('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5))
kolmogorov_smirnov.test('runsup', dict(samsize=14400, bins=6, confidence=0.95))
kolmogorov_smirnov.test('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99))
kolmogorov_smirnov.test('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))


