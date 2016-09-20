"""
Experiment: Univariate Test of Uniformity
"""

from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from rnd.randomness.uniformity_univariate import statistics, critical_min, critical_max, error, plot
from tests.experiments.randomness import PLOT_DIR, PLOT_EXT


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
    data = statistics(GENERATOR, STREAMS, SAMSIZE, BINS)

    # Critical Bounds
    mn = critical_min(BINS, CONFIDENCE)
    mx = critical_max(BINS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = error(data, mn, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    print('======================================')
    print('TEST OF UNIFORMITY - UNIVARIATE       ')
    print('======================================')
    print('Generator: %s' % GENERATOR.__class__.__name__)
    print('Streams: %d' % STREAMS)
    print('Seed: %d' % SEED)
    print('--------------------------------------')
    print('Sample Size: %d' % SAMSIZE)
    print('Bins: %d' % BINS)
    print('Confidence: %+.3f %%' % (CONFIDENCE * 100))
    print('--------------------------------------')
    print('Critical Lower Bound: %+.3f %%' % mn)
    print('Critical Upper Bound: %+.3f %%' % mx)
    print('--------------------------------------')
    print('Theoretical Error: %d (%.3f %%)' % (err['err_thr'], err['err_thr_perc'] * 100))
    print('Empirical Error: %d (%.3f %%)' % (err['err_emp'], err['err_emp_perc'] * 100))
    print('\tError(s) Min: %d (%.3f %%)' % (err['err_mn'], err['err_mn_perc'] * 100))
    print('\tError(s) Max: %d (%.3f %%)' % (err['err_mx'], err['err_mx_perc'] * 100))
    print('--------------------------------------')
    print('Result: ' + ('Not Failed' if res else 'Failed'))
    print('Summary: %.3f %% error (%+.3f %% of theoretical error)' % (err['err_emp_perc'] * 100, err['err_emp_thr_perc'] * 100))
    print('Suggested Confidence: %.3f %%' % (sugg_confidence * 100))
    print('\n')

    # Plot
    filename = '%s/%s.%s' % (PLOT_DIR, 'test_uniformity_univariate', PLOT_EXT)
    plot(data, mn, mx, filename=filename)


if __name__ == '__main__':
    experiment()