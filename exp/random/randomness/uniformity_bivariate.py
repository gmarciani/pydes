"""
Experiment: Bivariate Test of Uniformity
"""

from core.random.rndgen import MarcianiMultiStream as RandomGenerator
from _ignore.randomness import uniformity_bivariate as test
from core.utils.report import SimpleReport
from exp import EXP_DIR, PLT_EXT, RES_EXT

# Generator
GENERATOR = RandomGenerator()

# Test Parameters
SAMSIZE = 100000
BINS = 100
CONFIDENCE = 0.95

# Result File
FILENAME = '{}/{}'.format(EXP_DIR, 'test-uniformity-univariate')


def experiment(generator=GENERATOR,
               samsize=SAMSIZE,
               bins=BINS,
               confidence=CONFIDENCE,
               filename=FILENAME
               ):

    # Test
    data = test.statistics(generator, generator.get_streams_number(), samsize, bins)

    # Critical Bounds
    mn = test.critical_min(bins, confidence)
    mx = test.critical_max(bins, confidence)

    # Theoretical/Empirical Error
    err = test.error(data, mn, mx, confidence)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    r = SimpleReport('TEST OF BIVARIATE UNIFORMITY')
    r.add('Generator', 'Class', generator.__class__.__name__)
    r.add('Generator', 'Streams', generator.get_streams_number())
    r.add('Generator', 'Seed', generator.get_initial_seed())
    r.add('Test Parameters', 'Sample Size', samsize)
    r.add('Test Parameters', 'Bins', bins)
    r.add('Test Parameters', 'Confidence', '%.3F' % (confidence * 100))
    r.add('Critical Bounds', 'Lower Bound', mn)
    r.add('Critical Bounds', 'Upper Bound', mx)
    r.add('Error', 'Theoretical',
          '%d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100))
    r.add('Error', 'Empirical',
          '%d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100))
    r.add('Error', 'Empirical Lower Bound',
          '%d (%.3f %%)' % (err['err_mn'], err['err_mn_perc'] * 100))
    r.add('Error', 'Empirical Upper Bound',
          '%d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100))
    r.add('Result', 'Confidence', '%.3f %%' % (sugg_confidence * 100))

    rep_filename = '{}.{}'.format(filename, RES_EXT)
    r.save_txt(rep_filename)

    print(r)

    # Plot
    fig_filename = '{}.{}'.format(filename, PLT_EXT)
    test.plot(data, mn, mx, filename=fig_filename)


if __name__ == '__main__':
    experiment()
