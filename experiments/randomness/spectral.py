"""
Experiment: Spectral Test of Randomness.
"""

from demule.rnd.randomness import spectral
from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def experiment():

    # Generator
    SEED = 1
    generator = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 100000 #2147483646

    # Test
    data = spectral.observations(generator.rnd, SAMSIZE)

    # Report
    report = \
        '======================================' + '\n' + \
        'SPECTRAL TEST                         ' + '\n' + \
        '======================================' + '\n' + \
        'Generator: %s' % (generator.__class__.__name__,) + '\n' + \
        'Seed: %d' % (SEED,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Sample Size: %d' % (SAMSIZE,)  + '\n' + \
        '--------------------------------------' + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s.%s' % (EXP_DIR, 'test-spectral', PLT_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'test-spectral', PLT_EXT)
    spectral.plot(data, filename=filename)

    # Plot (with zoom)
    filename = '%s/%s.%s' % (EXP_DIR, 'test-spectral_zoom', PLT_EXT)
    spectral.plot(data, filename=filename, zoom=(0.5, 0.6))


if __name__ == '__main__':
    experiment()
