from plots.spectral import scatter2D


SAMSIZE = 10000 # SAMSIZE >= 10000


def observations(uniform, samsize=SAMSIZE):
    observed = []
    u1 = uniform()
    for _ in range(samsize - 1):
        u2 = uniform()
        observed.append((u1, u2))
        u1 = u2

    return observed


def plot(data, title=None, filename=None, zoom=None):
    scatter2D(data, title, filename, zoom)