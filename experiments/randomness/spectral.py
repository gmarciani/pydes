"""
Experiment: Spectral Test of Randomness.
"""

from core.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from core.rnd.randomness import spectral as test
from core.utils.report import SimpleReport
from experiments import EXP_DIR, PLT_EXT, RES_EXT

# Generator
GENERATOR = RandomGenerator()

# Test Parameters
SAMSIZE = 100000

# Plot
FILENAME = '{}/{}'.format(EXP_DIR, 'test-spectral')


def experiment(generator=GENERATOR,
               samsize=SAMSIZE,
               filename=FILENAME):

    # Test
    data = test.observations(GENERATOR.rnd, SAMSIZE)

    # Report
    r = SimpleReport('SPECTRAL TEST')
    r.add('Generator', 'Class', generator.__class__.__name__)
    r.add('Generator', 'Seed', generator.get_initial_seed())
    r.add('Test Parameters', 'Sample Size', samsize)

    rep_filename = '{}.{}'.format(filename, RES_EXT)
    r.save(rep_filename)

    print(r)

    # Plot
    fig_filename = '{}.{}'.format(filename, PLT_EXT)
    test.plot(data, filename=fig_filename)

    # Plot (with zoom)
    fig_filename = '{}-zoom.{}'.format(filename, PLT_EXT)
    test.plot(data, filename=fig_filename, zoom=(0.5, 0.6))


if __name__ == '__main__':
    experiment()
