"""
Experiment: Univariate Test of Uniformity
"""

from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.rnd.randomness import uniformity_univariate
from demule.utils.report import SimpleReport
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def experiment():

    # Generator
    SEED = 1
    STREAMS = 256
    GENERATOR = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 10000
    BINS = 1000
    CONFIDENCE = 0.95

    # Test
    data = uniformity_univariate.statistics(GENERATOR, STREAMS, SAMSIZE, BINS)

    # Critical Bounds
    mn = uniformity_univariate.critical_min(BINS, CONFIDENCE)
    mx = uniformity_univariate.critical_max(BINS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = uniformity_univariate.error(data, mn, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    r = SimpleReport('TEST OF UNIVARIATE UNIFORMITY')
    r.add('Generator', 'Class', GENERATOR.__class__.__name__)
    r.add('Generator', 'Streams', STREAMS)
    r.add('Generator', 'Seed', SEED)
    r.add('Test Parameters', 'Sample Size', SAMSIZE)
    r.add('Test Parameters', 'Bins', BINS)
    r.add('Test Parameters', 'Confidence', '%.3F' % (CONFIDENCE * 100))
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

    r.save('%s/%s.%s' % (EXP_DIR, 'test-uniformity-univariate', RES_EXT))

    print(r)

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'test_uniformity_univariate', PLT_EXT)
    uniformity_univariate.plot(data, mn, mx, filename=filename)


if __name__ == '__main__':
    experiment()