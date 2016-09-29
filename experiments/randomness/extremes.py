"""
Experiment: Extremes Test of Uniformity.
"""

from demule.rnd.randomness import extremes
from demule.rnd.rndgen import MarcianiMultiStream as RandomGenerator
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
    D = 5
    CONFIDENCE = 0.95

    # Test
    data = extremes.statistics(GENERATOR, STREAMS, SAMSIZE, BINS, D)

    # Critical Bounds
    mn = extremes.critical_min(BINS, CONFIDENCE)
    mx = extremes.critical_max(BINS, CONFIDENCE)

    # Theoretical/Empirical Error
    err = extremes.error(data, mn, mx, CONFIDENCE)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    r = SimpleReport('TEST OF EXTREMES')
    r.add('Generator', 'Class', GENERATOR.__class__.__name__)
    r.add('Generator', 'Streams', STREAMS)
    r.add('Generator', 'Seed', SEED)
    r.add('Test Parameters', 'Sample Size', SAMSIZE)
    r.add('Test Parameters', 'Bins', BINS)
    r.add('Test Parameters', 'Confidence', '%.3F' % (CONFIDENCE * 100))
    r.add('Test Parameters', 'D', D)
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

    r.save('%s/%s.%s' % (EXP_DIR, 'test-extremes', RES_EXT))

    print(r)

    # Plot
    filename = '%s/%s.%s' % (EXP_DIR, 'test-extremes', PLT_EXT)
    extremes.plot(data, mn, mx, filename=filename)


if __name__ == '__main__':
    experiment()