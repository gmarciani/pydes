"""
Experiment: Bivariate correlation
"""

import unittest
from core.random.rndgen import MarcianiMultiStream as RandomGenerator
from _ignore.plots import scatter
from tests import RES_DIR, PLT_EXT


class PlotsTest(unittest.TestCase):

    def test_bivariate_scatterplot(self):

        rndgen = RandomGenerator(1)

        sample_size = 100

        sample = []
        for _ in range(sample_size):
            u = rndgen.rnd()
            v = u ** 10
            sample.append((u, v))

        # Plot
        filename = '%s/%s.%s' % (RES_DIR, 'bivariate-scatterplot', PLT_EXT)
        scatter.bivariate_scatterplot(sample, filename=filename)


if __name__ == '__main__':
    unittest.main()
