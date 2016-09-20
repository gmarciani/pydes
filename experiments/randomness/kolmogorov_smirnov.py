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
    report = \
        '======================================' + '\n' + \
        'TEST OF KOLMOGOROV-SMIRNOV            ' + '\n' + \
        '======================================' + '\n' + \
        'Chi-Square Test: %s' % (testname,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Generator: %s' % (GENERATOR.__class__.__name__,) + '\n' + \
        'Streams: %d' % (STREAMS,) + '\n' + \
        'Seed: %d' % (SEED,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Sample Size: %d' % (SAMSIZE,) + '\n' + \
        'Bins: %d' % (BINS,) + '\n'
    if testname is 'extremes':
        report += 'D: %d' % (params['d'],)
    elif testname is 'gap':
        report += 'A: %d' % (params['a'],)
        report += 'B: %d' % (params['b'],)
    elif testname is 'permutation':
        report += 'T: %d' % (params['t'],)
    report += \
        'Confidence: %+.3f %%' % (CONFIDENCE * 100,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'KS-Statistic: %.3f' % (ksstat,) + '\n' + \
        'Critical Upper Bound: %.3f' % (mx,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Theoretical Error: %d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100) + '\n' + \
        'Empirical Error: %d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100) + '\n' + \
        '\tError(s) Max: %d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Result: ' + ('Not Failed' if res else 'Failed') + '\n' + \
        'Summary: %.3f %% error (%+.3f %% of theoretical error)' % (
        err['err_emp_perc'] * 100, err['err_emp_thr_perc'] * 100) + '\n' + \
        'Suggested Confidence: %.3f %%' % (sugg_confidence * 100) + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s-%s.%s' % (EXP_DIR, 'test-ks', testname, RES_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)

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