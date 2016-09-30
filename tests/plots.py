"""
Experiment: Bivariate correlation
"""

import unittest
from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.plots import scatter
from tests import RES_DIR, PLT_EXT


class PlotsTest(unittest.TestCase):

    def test_bivariate_scatterplot(self):

        GENERATOR = RandomGenerator(1)

        SAMSIZE = 100

        sample = []
        for _ in range(SAMSIZE):
            u = GENERATOR.rnd()
            v = u ** 10
            sample.append((u, v))

        # Plot
        filename = '%s/%s.%s' % (RES_DIR, 'bivariate-scatterplot', PLT_EXT)
        scatter.bivariate_scatterplot(sample, filename=filename)


if __name__ == '__main__':
    unittest.main()
