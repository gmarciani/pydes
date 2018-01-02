"""
Experiment: Kolmogorov-Smirnov test.
"""

from core.rnd.rndgen import MarcianiMultiStream as RandomGenerator
from core.rnd.randomness import kolmogorov_smirnov as test
from core.rnd.randomness import extremes
from core.rnd.randomness import gap
from core.rnd.randomness import permutation
from core.rnd.randomness import runsup
from core.rnd.randomness import uniformity_bivariate
from core.rnd.randomness import uniformity_univariate
from core.utils.report import SimpleReport
from experiments import EXP_DIR, PLT_EXT, RES_EXT


# Result File
FILENAME = '{}/{}'.format(EXP_DIR, 'test-ks')


def experiment(generator, testname, params, filename=FILENAME):

    samsize = params['samsize']
    bins = params['bins']
    confidence = params['confidence']

    streams = generator.get_streams_number()

    if testname is 'uniformity_u':
        data = uniformity_univariate.statistics(generator, streams, samsize, bins)
    elif testname is 'uniformity_b':
        data = uniformity_bivariate.statistics(generator, streams, samsize, bins)
    elif testname is 'extremes':
        data = extremes.statistics(generator, streams, samsize, bins, params['d'])
    elif testname is 'runsup':
        data = runsup.statistics(generator, streams, samsize, bins)
    elif testname is 'gap':
        data = gap.statistics(generator, streams, samsize, bins, params['a'], params['b'])
    elif testname is 'permutation':
        data = permutation.statistics(generator, streams, samsize, bins, params['t'])
    else:
        raise ValueError('%s is not a valid testname' % testname)

    # Test
    distances = test.ksdistances(data, bins)
    kspnt = test.kspoint(distances)
    ksstat = test.ksstatistic(distances)

    # Critical Bound
    mx = test.critical_ksdistance(streams, confidence)

    # Theoretical/Empirical Error
    err = test.error(distances, mx, confidence)

    # Result
    res = err['err_emp'] <= err['err_thr']
    sugg_confidence = 1 - err['err_emp_perc']

    # Report
    r = SimpleReport('TEST OF KOLMOGOROV-SMIRNOV')
    r.add('Generator', 'Class', generator.__class__.__name__)
    r.add('Generator', 'Streams', streams)
    r.add('Generator', 'Seed', generator.get_initial_seed())
    r.add('Test Parameters', 'Chi-Square Test', testname)
    r.add('Test Parameters', 'Sample Size', samsize)
    r.add('Test Parameters', 'Bins', bins)
    r.add('Test Parameters', 'Confidence', '%.3F' % (confidence * 100))
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

    rep_filename = '{}.{}'.format(filename, RES_EXT)
    r.save(rep_filename)

    print(r)

    # Plot (Type 1)
    fig_filename = '{}-{}.{}'.format(filename, testname, PLT_EXT)
    test.plot(distances, kspnt, mx, filename=fig_filename)

    # Plot (Type 2)
    fig_filename = '{}-{}-2.{}'.format(filename, testname, PLT_EXT)
    test.plot2(data, bins, kspnt, filename=fig_filename)


if __name__ == '__main__':

    tests = [
        ('uniformity_u', dict(samsize=10000, bins=1000, confidence=0.95)),
        ('uniformity_b', dict(samsize=100000, bins=100, confidence=0.95)),
        ('extremes', dict(samsize=10000, bins=1000, confidence=0.95, d=5)),
        ('runsup', dict(samsize=14400, bins=6, confidence=0.95)),
        ('gap', dict(samsize=10000, bins=78, confidence=0.95, a=0.94, b=0.99)),
        ('permutation', dict(samsize=7200, bins=720, confidence=0.95, t=6))
    ]

    for t in tests:
        experiment(RandomGenerator(), t[0], t[1])