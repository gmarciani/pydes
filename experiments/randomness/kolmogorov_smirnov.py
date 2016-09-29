"""
Experiment: Kolmogorov-Smirnov test.
"""

from demule.rnd.randomness import extremes
from demule.rnd.randomness import gap
from demule.rnd.randomness import kolmogorov_smirnov
from demule.rnd.randomness import permutation
from demule.rnd.randomness import runsup
from demule.rnd.randomness import uniformity_bivariate
from demule.rnd.randomness import uniformity_univariate
from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.utils.report import SimpleReport
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def test(testname, params):

    # Generator
    SEED = 1
    STREAMS = 256
    GENERATOR = RandomGenerator(SEED)

    # General parameters
    SAMSIZE = params['samsize']
    BINS = params['bins']
    CONFIDENCE = params['confidence']

    if testname is 'uniformity_univariate':
        data = uniformity_univariate.statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'uniformity_bivariate':
        data = uniformity_bivariate.statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'extremes':
        data = extremes.statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['d'])
    elif testname is 'runsup':
        data = runsup.statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'gap':
        data = gap.statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['a'], params['b'])
    elif testname is 'permutation':
        data = permutation.statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['t'])
    else:
        raise ValueError('%s is not a valid testname' % testname)

    # Test
    distances = kolmogorov_smirnov.ksdistances(data, BINS)
    kspnt = kolmogorov_smirnov.kspoint(distances)
    ksstat = kolmogorov_smirnov.ksstatistic(distances)

    # Critical Bound
    mx = kolmogorov_smirnov.critical_ksdistance(STREAMS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = kolmogorov_smirnov.error(distances, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    r = SimpleReport('TEST OF KOLMOGOROV-SMIRNOV')
    r.add('Generator', 'Class', GENERATOR.__class__.__name__)
    r.add('Generator', 'Streams', STREAMS)
    r.add('Generator', 'Seed', SEED)
    r.add('Test Parameters', 'Chi-Square Test', testname)
    r.add('Test Parameters', 'Sample Size', SAMSIZE)
    r.add('Test Parameters', 'Bins', BINS)
    r.add('Test Parameters', 'Confidence', '%.3F' % (CONFIDENCE * 100))
    if testname is 'extremes':
        r.add('Test Parameters', 'D', params['d'])
    elif testname is 'gap':
        r.add('Test Parameters', 'A', params['a'])
        r.add('Test Parameters', 'B', params['b'])
    elif testname is 'permutation':
        r.add('Test Parameters', 'T', params['t'])
    r.add('Critical Bounds', 'KS Statistic', '%.3F' % ksstat)
    r.add('Critical Bounds', 'Upper Bound', '%.3F' % mx)
    r.add('Error', 'Theoretical',
          '%d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100))
    r.add('Error', 'Empirical',
          '%d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100))
    r.add('Error', 'Empirical Upper Bound',
          '%d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100))
    r.add('Result', 'Confidence', '%.3f %%' % (sugg_confidence * 100))

    r.save('%s/%s.%s' % (EXP_DIR, 'test-ks', RES_EXT))

    print(r)

    # Plot
    filename = '%s/%s-%s.%s' % (EXP_DIR, 'test-ks', testname, PLT_EXT)
    kolmogorov_smirnov.plot(distances, kspnt, mx, filename=filename)

    filename = '%s/%s-%s-2.%s' % (EXP_DIR, 'test-ks', testname, PLT_EXT)
    kolmogorov_smirnov.plot2(data, BINS, kspnt, filename=filename)


if __name__ == '__main__':

    test('uniformity_univariate', dict(samsize=10000, bins=1000, confidence=0.95))

    #test('uniformity_bivariate', dict(samsize=100000, bins=100, confidence=0.95))

    #test('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5))

    #test('runsup', dict(samsize=14400, bins=6, confidence=0.95))

    #test('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99))

    #test('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))