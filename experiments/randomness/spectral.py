"""
Experiment: Spectral Test of Randomness.
"""

from demule.rnd.randomness import spectral
from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.utils.report import SimpleReport
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def experiment():

    # Generator
    SEED = 1
    GENERATOR = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 100000 #2147483646

    # Test
    data = spectral.observations(GENERATOR.rnd, SAMSIZE)

    # Report
    r = SimpleReport('SPECTRAL TEST')
    r.add('Generator', 'Class', GENERATOR.__class__.__name__)
    r.add('Generator', 'Seed', SEED)
    r.add('Test Parameters', 'Sample Size', SAMSIZE)

    r.save('%s/%s.%s' % (EXP_DIR, 'test-spectral', PLT_EXT))

    print(r)

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'test-spectral', PLT_EXT)
    spectral.plot(data, filename=filename)

    # Plot (with zoom)
    filename = '%s/%s.%s' % (EXP_DIR, 'test-spectral_zoom', PLT_EXT)
    spectral.plot(data, filename=filename, zoom=(0.5, 0.6))


if __name__ == '__main__':
    experiment()
