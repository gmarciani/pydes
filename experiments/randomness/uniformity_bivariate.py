"""
Experiment: Bivariate Test of Uniformity
"""

from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from demule.rnd.randomness import uniformity_bivariate
from experiments import EXP_DIR, PLT_EXT, RES_EXT


def experiment():

    # Generator
    SEED = 1
    STREAMS = 256
    GENERATOR = RandomGenerator(SEED)

    # Test Parameters
    SAMSIZE = 100000
    BINS = 100
    CONFIDENCE = 0.95

    # Test
    data = uniformity_bivariate.statistics(GENERATOR, STREAMS, SAMSIZE, BINS)

    # Critical Bounds
    mn = uniformity_bivariate.critical_min(BINS, CONFIDENCE)
    mx = uniformity_bivariate.critical_max(BINS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = uniformity_bivariate.error(data, mn, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    report = \
        '======================================' + '\n' + \
        'TEST OF UNIFORMITY - BIVARIATE        ' + '\n' + \
        '======================================' + '\n' + \
        'Generator: %s' % (GENERATOR.__class__.__name__,) + '\n' + \
        'Streams: %d' % (STREAMS,) + '\n' + \
        'Seed: %d' % (SEED,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Sample Size: %d' % (SAMSIZE,) + '\n' + \
        'Bins: %d' % (BINS,) + '\n' + \
        'Confidence: %+.3f %%' % (CONFIDENCE * 100,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Critical Lower Bound: %+.3f %%' % (mn,) + '\n' + \
        'Critical Upper Bound: %+.3f %%' % (mx,) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Theoretical Error: %d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100) + '\n' + \
        'Empirical Error: %d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100) + '\n' + \
        '\tError(s) Min: %d (%.3f %%)' % (err['err_mn'], err['err_mn_perc'] * 100) + '\n' + \
        '\tError(s) Max: %d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100) + '\n' + \
        '--------------------------------------' + '\n' + \
        'Result: ' + ('Not Failed' if res else 'Failed') + '\n' + \
        'Summary: %.3f %% error (%+.3f %% of theoretical error)' % (err['err_emp_perc'] * 100, err['err_emp_thr_perc'] * 100) + '\n' + \
        'Suggested Confidence: %.3f %%' % (sugg_confidence * 100) + '\n\n'

    print(report)

    # Report on file
    filename = '%s/%s.%s' % (EXP_DIR, 'test-uniformity-bivariate', RES_EXT)
    with open(filename, 'w') as resfile:
        resfile.write(report)

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'test_uniformity_bivariate', PLT_EXT)
    uniformity_bivariate.plot(data, mn, mx, filename=filename)


if __name__ == '__main__':
    experiment()
