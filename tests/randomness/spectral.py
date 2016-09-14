from rnd.generators.lehemers import LehmerMultiStream as Lehmer
from rnd.tests.spectral import observations, plot


def test():

    # Parameters
    SAMSIZE = 2147483646

    # Generator
    SEED = 1
    generator = Lehmer(SEED)

    # Test
    data = observations(generator.rnd, SAMSIZE)

    # Report (Object)
    report = dict(
        test_name='TEST OF SPECTRUM',

        generator=generator.__class__.__name__,
        seed=SEED,

        samsize=SAMSIZE
    )

    # Report (Printed)
    print('--------------------------------------')
    print('# TEST OF SPECTRUM                   #')
    print('--------------------------------------')
    print('Generator: ' + generator.__class__.__name__)
    print('Seed: ' + str(SEED))
    print('--------------------------------------')
    print('Sample Size: ' + str(SAMSIZE))
    print('--------------------------------------')
    print('\n')

    # Plot
    plot('Test of Spectrum', data, filename='../resources/randomness/test-spectrum.png')

    return report


if __name__ == '__main__':
    test()
