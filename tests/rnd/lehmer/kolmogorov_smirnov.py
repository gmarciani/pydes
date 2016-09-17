from rnd.lehmer.lehemers import LehmerMultiStream as Lehmer
from rnd.tests.kolmogorov_smirnov import ksdistances, kspoint, ksstatistic, critical_ksdistance, error, plot, plot2
from rnd.tests.uniformity_univariate import statistics as uunivariate_statistics
from rnd.tests.uniformity_bivariate import statistics as ubivariate_statistics
from rnd.tests.extremes import statistics as extremes_statistics
from rnd.tests.runsup import statistics as runsup_statistics
from rnd.tests.gap import statistics as gap_statistics
from rnd.tests.permutation import statistics as permutation_statistics
from tests.rnd.lehmer import PLOT_DIR, PLOT_EXT


def test(testname, params):

    # Generator
    SEED = 1
    STREAMS = 256
    GENERATOR = Lehmer(SEED)

    # General parameters
    SAMSIZE = params['samsize']
    BINS = params['bins']
    CONFIDENCE = params['confidence']

    if testname is 'uniformity_univariate':
        data = uunivariate_statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'uniformity_bivariate':
        data = ubivariate_statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'extremes':
        data = extremes_statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['d'])
    elif testname is 'runsup':
        data = runsup_statistics(GENERATOR, STREAMS, SAMSIZE, BINS)
    elif testname is 'gap':
        data = gap_statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['a'], params['b'])
    elif testname is 'permutation':
        data = permutation_statistics(GENERATOR, STREAMS, SAMSIZE, BINS, params['t'])
    else:
        raise ValueError('%s is not a valid testname' % testname)

    # Test
    distances = ksdistances(data, BINS)
    kspnt = kspoint(distances)
    ksstat = ksstatistic(distances)

    # Critical Bound
    mx = critical_ksdistance(STREAMS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = error(distances, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    print('======================================')
    print('TEST OF KOLMOGOROV-SMIRNOV            ')
    print('======================================')
    print('Chi-Square Test: %s' % testname)
    print('--------------------------------------')
    print('Generator: %s' % GENERATOR.__class__.__name__)
    print('Streams: %d' % STREAMS)
    print('Seed: %d' % SEED)
    print('--------------------------------------')
    print('Sample Size: %d' % SAMSIZE)
    print('Bins: %d' % BINS)
    if testname is 'extremes':
        print('D: %d' % params['d'])
    elif testname is 'gap':
        print('A: %d' % params['a'])
        print('B: %d' % params['b'])
    elif testname is 'permutation':
        print('T: %d' % params['t'])
    print('Confidence: %+.3f %%' % (CONFIDENCE * 100))
    print('--------------------------------------')
    print('KS-Statistic: %.3f' % ksstat)
    print('Critical Upper Bound: %.3f' % mx)
    print('--------------------------------------')
    print('Theoretical Error: %d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100))
    print('Empirical Error: %d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100))
    print('\tError(s) Max: %d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100))
    print('--------------------------------------')
    print('Result: ' + ('Not Failed' if res else 'Failed'))
    print('Summary: %.3f %% error (%+.3f %% of theoretical error)' % (
    err['err_emp_perc'] * 100, err['err_emp_thr_perc'] * 100))
    print('Suggested Confidence: %.3f %%' % (sugg_confidence * 100))
    print('\n')

    # Plot
    filename = '%s/%s-%s.%s' % (PLOT_DIR, 'test-ks', testname, PLOT_EXT)
    plot(distances, kspnt, mx, filename=filename)

    filename = '%s/%s-%s-2.%s' % (PLOT_DIR, 'test-ks', testname, PLOT_EXT)
    plot2(data, BINS, kspnt, filename=filename)


if __name__ == '__main__':

    test('uniformity_univariate', dict(samsize=10000, bins=1000, confidence=0.95))

    #test('uniformity_bivariate', dict(samsize=100000, bins=100, confidence=0.95))

    #test('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5))

    #test('runsup', dict(samsize=14400, bins=6, confidence=0.95))

    #test('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99))

    #test('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))