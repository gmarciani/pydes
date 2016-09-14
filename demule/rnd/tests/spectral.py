from plots.spectral import scatter2D as spectral_scatter


# hint: samsize >= 10000


def observations(uniform, samsize):
    observed = []
    u1 = uniform()
    for _ in range(samsize - 1):
        u2 = uniform()
        observed.append((u1, u2))
        u1 = u2

    return observed


def plot(title, data, filename=None):
    spectral_scatter(title, data, filename)