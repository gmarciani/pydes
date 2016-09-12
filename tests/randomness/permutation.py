from controls.randomness.permutation import observations, chisquare, critical_min, critical_max
from models.generators.lehemers import LehmerMultiStream as Lehmer


def test():

    # Parameters
    SAMSIZE = 7200
    STREAMS = 256
    BINS = 720
    T = 6
    CONFIDENCE = 0.95

    PRECISION = '.3f'

    # Generator
    SEED = 1
    generator = Lehmer(SEED)

    # Test
    data = []
    for stream in range(STREAMS):
        generator.stream(stream)
        observed = observations(generator.rnd, SAMSIZE, BINS, T)
        chi = chisquare(observed, SAMSIZE)
        result = (stream, chi)
        data.append(result)

    # Critical Bounds
    mn = critical_min(BINS, CONFIDENCE)
    mx = critical_max(BINS, CONFIDENCE)

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
        t=T,

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
    print('# TEST OF INDEPENDENCE - PERMUTATION #')
    print('--------------------------------------')
    print('Generator: ' + generator.__class__.__name__)
    print('Seed: ' + str(SEED))
    print('--------------------------------------')
    print('Sample Size: ' + str(SAMSIZE))
    print('Streams: ' + str(STREAMS))
    print('Bins: ' + str(BINS))
    print('T: ' + str(T))
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
    #py.plot(figure, filename='../resources/randomness/test-independence-permutation.html')

    return report


if __name__ == '__main__':
    test()