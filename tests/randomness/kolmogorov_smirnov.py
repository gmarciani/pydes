from controls.randomness.uniformity_univariate import observations, chisquare
from controls.randomness.kolmogorov_smirnov import ksdistances, critical_ksdistance
from models.generators.lehemers import LehmerMultiStream as Lehmer


def test_uniformity_univariate():

    # Parameters
    SAMSIZE = 10000
    STREAMS = 256
    BINS = 1000
    CONFIDENCE = 0.95

    PRECISION = '.3f'

    # Generator
    SEED = 1
    generator = Lehmer(SEED)

    # Test
    statistics = []
    for stream in range(STREAMS):
        generator.stream(stream)
        observed = observations(generator.rnd, SAMSIZE, BINS)
        chi = chisquare(observed, SAMSIZE)
        statistics.append(chi)
    distances = ksdistances(statistics)

    # Critical Bounds
    mx = critical_ksdistance(STREAMS, CONFIDENCE)

    # Theoretical Error
    err_thr = round((1 - CONFIDENCE) * STREAMS)
    err_thr_perc = err_thr / STREAMS

    # Empirical Error
    err_mn = 0
    err_mx = 0
    for value in data:
        if value[1] < mn:
            err_mn += 1
        elif value[1] > mx:
            err_mx += 1
    err_emp = err_mn + err_mx
    err_mn_perc = err_mn / STREAMS
    err_mx_perc = err_mn / STREAMS
    err_emp_perc = err_emp / STREAMS
    err_emp_thr_perc = (err_emp - err_thr) / err_thr
    sugg_confidence = 1 - err_emp_perc

    # Result
    res = err_emp <= err_thr

    # Report (Object)
    report = dict(
        test_name='TEST OF UNIFORMITY - UNIVARIATE',

        generator=generator.__class__.__name__,
        seed=SEED,

        samsize=SAMSIZE,
        streams=STREAMS,
        bins=BINS,
        confidence=CONFIDENCE,

        mn=mn,
        mx=mx,

        err_thr=err_thr,
        err_emp=err_emp,
        err_mn=err_mn,
        err_mx=err_mx,

        err_thr_perc=err_thr_perc,
        err_emp_perc=err_emp_perc,
        err_mn_perc=err_mn_perc,
        err_mx_perc=err_mx_perc,
        err_emp_thr_perc=err_emp_thr_perc,

        sugg_confidence=sugg_confidence,

        result=res
    )

    # Report (Printed)
    print('--------------------------------------')
    print('# KS - UNIFORMITY - UNIVARIATE       #')
    print('--------------------------------------')
    print('Generator: ' + generator.__class__.__name__)
    print('Seed: ' + str(SEED))
    print('--------------------------------------')
    print('Sample Size: ' + str(SAMSIZE))
    print('Streams: ' + str(STREAMS))
    print('Bins: ' + str(BINS))
    print('Confidence: ' + format(CONFIDENCE * 100, PRECISION) + '%')
    print('--------------------------------------')
    print('Critical Lower Bound: ' + format(mn, PRECISION))
    print('Critical Upper Bound: ' + format(mx, PRECISION))
    print('--------------------------------------')
    print('Theoretical Error: ' + str(err_thr) + ' (' + format(err_thr_perc * 100, PRECISION) + '%)')
    print('Empirical Error: ' + str(err_emp) + ' (' + format(err_emp_perc * 100, PRECISION) + '%)')
    print('\tError(s) Min: ' + str(err_mn) + ' (' + format(err_mn_perc * 100, PRECISION) + '%)')
    print('\tError(s) Max: ' + str(err_mx) + ' (' + format(err_mx_perc * 100, PRECISION) + '%)')
    print('--------------------------------------')
    print('Result: ' + ('Not Failed' if res else 'Failed'))
    print('Summary: ' + format(err_emp_perc * 100, PRECISION) + '% error' +
          ' (' + format(err_emp_thr_perc * 100, '+'+PRECISION) + '% w.r.t. theoretical error)')
    print('Suggested Confidence: ' + format(sugg_confidence * 100, PRECISION) + '%')
    print('\n')

    # Plot
    #figure = plot(data, mn, mx)
    #py.plot(figure, filename='../resources/randomness/test-uniformity-univariate.html')

    return report


if __name__ == '__main__':
    test()