from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.rnd.randomness import spectral
from tests.rnd.randomness import PLOT_DIR, PLOT_EXT


def test():

    # Generator
    SEED = 1
    generator = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 10000 #2147483646

    # Test
    data = spectral.observations(generator.rnd, SAMSIZE)

    # Report
    print('======================================')
    print('SPECTRAL TEST                         ')
    print('======================================')
    print('Generator: %s' % generator.__class__.__name__)
    print('Seed: %d' % SEED)
    print('--------------------------------------')
    print('Sample Size: %d' % SAMSIZE)
    print('--------------------------------------')
    print('\n')

    # Plot
    filename = '%s/%s.%s' % (PLOT_DIR, 'spectral_test', PLOT_EXT)
    spectral.plot(data, filename=filename)

    filename = '%s/%s.%s' % (PLOT_DIR, 'spectral_test_zoom', PLOT_EXT)
    spectral.plot(data, filename=filename, zoom=(0.5, 0.6))


if __name__ == '__main__':
    test()
