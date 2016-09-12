from controls.plots.randomness_plots import scatter
from controls.statistics import chisquare_univariate
from libs.des.rvms import idfChisquare


# hint: samsize >= 10*bins, bins = t!, t > 3, confidence = 0.95,


def observations(uniform, samsize, bins, t):
    observed = [0] * bins

    for i in range(samsize):
        U = [uniform() for _ in range(t)]
        r = t - 1
        b = 0
        while r > 0:
            mx = 0
            for j in range(1,r + 1):
                if U[j] > U[mx]:
                    mx = j
            b = (r + 1) * b + mx
            U[mx], U[r] = U[r], U[mx]
            r -= 1
        observed[b] += 1

    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def plot(data, min, max):
    title = 'Test of Independence (Permutation)'
    figure = scatter(title, data, min, max)
    return figure