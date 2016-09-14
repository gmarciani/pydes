def chisquare_univariate(observed, expected, start=0):
    K = len(observed)
    value = 0
    for x in range(start, K):
        value += ((observed[x] - expected(x)) ** 2) / expected(x)
    return value


def chisquare_bivariate(observed, expected, start=0):
    K = len(observed)
    value = 0
    for x1 in range(start, K):
        for x2 in range(start, K):
            value += ((observed[x1][x2] - expected(x1, x2)) ** 2) / expected(x1, x2)
    return value