"""
Experiment: Bivariate correlation
"""

from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.plots import scatter
from experiments import EXP_DIR, PLT_EXT


def experiment():

    # Generator
    SEED = 1
    GENERATOR = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 100

    sample = []
    for _ in range(SAMSIZE):
        u = GENERATOR.rnd()
        v = u ** 10
        sample.append((u, v))

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'bivariate-scatterplot', PLT_EXT)
    scatter.bivariate_scatterplot(sample, filename=filename)


if __name__ == '__main__':
    experiment()