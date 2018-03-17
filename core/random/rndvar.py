"""
Random variates.
"""


from enum import Enum, unique
from math import log, sqrt, exp


def bernoulli(p, u):
    """
    Generates a Bernoulli random variate.
    :param p: (float) success probability. Must be 0.0 < p < 1.0.
    :param u: (float) random number in (0,1).
    :return: (float) the Bernoulli(p) random variate.
    """
    return 0 if u < (1-p) else 1


def binomial(n, p, u):
    """
    Generates a Binomial random variate.
    :param n: (int) the cardinality. Must be n > 0.
    :param p: (float) success probability. Must be 0.0 < p < 1.0.
    :param u: (float) random number in (0,1).
    :return: (float) the Binomial(n,p) random variate.
    """
    x = 0
    for i in range(0, n):
        x += bernoulli(p, u)
    return x


def chisquare(n, u):
    """
    Generates a Chi Square random variate.
    :param n: (int) degree of freedom. Must be n > 0.
    :param u: (float) random number in (0,1).
    :return: (float) the ChiSquare(n) random variate.
    """
    x = 0.0
    for i in range(0, n):
        z = normal(0.0, 1.0, u)
        x += z * z
    return x


def equilikely(a, b, u):
    """
    Generates an Equilikely random variate in *[a,b]*.
    Must be a < b.
    :param a: (int) lower bound.
    :param b: (int) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Equilikely(a,b) random variate.
    """
    return a + int((b - a + 1) * u)


def erlang(n, b, u):
    """
    Generates an Erlang random variate.
    :param n: (int) parameter n. Must be n > 0.
    :param b: (float) parameter b. Must be b > 0.0.
    :param u: (float) random number in (0,1).
    :return: (float) the Erlang(n,b) random variate.
    """
    x = 0.0
    for i in range(0, n):
        x += exponential(b, u)
    return x


def exponential(m, u):
    """
    Generates an Exponential random variate with average *m*.
    :param m: (float) average of the distribution; must be m > 0.0
    :param u: (float) random number in (0,1).
    :return: (float) the Exp(m) random variate.
    """
    return -m * log(1.0 - u)


def geometric(p, u):
    """
    Generates a Geometric random variate with parameter *p*.
    :param p: (float) parameter of the distribution; must be 0.0 < p < 1.0
    :param u: (float) random number in (0,1).
    :return: (float) the Geom(p) random variate.
    """
    return int(log(1.0 - u) / log(p))


def lognormal(a, b, u):
    """
    Generates a Lognormal random variate.
    :param a: (float) lower bound.
    :param b: (float) upper bound. Must be b > 0.0
    :param u: (float) random number in (0,1).
    :return: (float) the Lognormal(a,b) random variate.
    """
    return exp(a + b * normal(0.0, 1.0, u))


def normal(m, s, u):
    """
    Generates a Normal random variate.
    :param m: (float) the mean.
    :param s: (float) the standard deviation. Must be s > 0.0.
    :param u: (float) random number in (0,1).
    :return: (float) the Normal(m,s) random variate.
    """
    p0 = 0.322232431088
    q0 = 0.099348462606
    p1 = 1.0
    q1 = 0.588581570495
    p2 = 0.342242088547
    q2 = 0.531103462366
    p3 = 0.204231210245e-1
    q3 = 0.103537752850
    p4 = 0.453642210148e-4
    q4 = 0.385607006340e-2

    if u < 0.5:
        t = sqrt(-2.0 * log(u))
    else:
        t = sqrt(-2.0 * log(1.0 - u))

    p = p0 + t * (p1 + t * (p2 + t * (p3 + t * p4)))
    q = q0 + t * (q1 + t * (q2 + t * (q3 + t * q4)))

    if u < 0.5:
        z = (p / q) - t
    else:
        z = t - (p / q)

    return m + s * z


def pascal(n, p, u):
    """
    Generates a Pascal random variate.
    :param n: (int) the parameter n. Must be n > 0.
    :param p: (float) the parameter p. Must be 0.0 < p < 1.0.
    :return: (float) the Pascal(n,p) random variate.
    """
    x = 0
    for i in range(0, n):
        x += geometric(p, u)
    return x


def poisson(m, u):
    """
    Generates a Poisson random variate.
    :param m: (float) the mean. Must be m > 0.
    :param u: (float) random number in (0,1).
    :return: (float) the Poisson(m) random variate.
    """
    t = 0.0
    x = 0
    while t < m:
        t += exponential(1.0, u)
        x += 1
    return x - 1


def student(n, u):
    """
    Generates a Student random variate.
    :param n: (int) degree of freedom. Must be n > 2.
    :param u: (float) random number in (0,1).
    :return: (float) the Student(n) random variate.
    """
    return normal(0.0, 1.0, u) / sqrt(chisquare(n, u) / n)


def uniform(a, b, u):
    """
    Generates a Uniform random variate in *(a,b)*.
    Must be a < b.
    :param a: (float) lower bound.
    :param b: (float) upper bound.
    :param u: (float) random number in (0,1).
    :return: (float) the Uniform(a,b) random variate.
    """
    return a + (b - a) * u


class VariateGenerator:
    """
    A generator of random variates.
    """

    def __init__(self, f):
        """
        Create a new instance of a VariateGenerator.
        :param f: (function) the function used to generate the random variate.
        """
        self.f = f

    def generate(self, u, **kwargs):
        """
        Generate a random variate value.
        :param u: a random generator.
        :param kwargs: distribution parameters.
        :return: the random value.
        """
        return self.f(u=u.rnd(), **kwargs)


class DeterministicGenerator:
    """
    A generator of deterministic number.
    """

    def generate(self, **kwargs):
        """
        Generate a random variate value.
        :param u: a random generator.
        :param kwargs: distribution parameters.
        :return: the random value.
        """
        return kwargs["v"]


@unique
class Variate(Enum):
    """
    Enumerate random variates.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, generator):
        self.generator = generator

    BERNOULLI = VariateGenerator(bernoulli)
    BINOMIAL = VariateGenerator(binomial)
    CHISQUARE = VariateGenerator(chisquare)
    DETERMINISTIC = DeterministicGenerator
    EQUILIKELY = VariateGenerator(equilikely)
    ERLANG = VariateGenerator(erlang)
    EXPONENTIAL = VariateGenerator(exponential)
    GEOMETRIC = VariateGenerator(geometric)
    LOGNORMAL = VariateGenerator(lognormal)
    NORMAL = VariateGenerator(normal)
    PASCAL = VariateGenerator(pascal)
    POISSON = VariateGenerator(poisson)
    STUDENT = VariateGenerator(student)
    UNIFORM = VariateGenerator(uniform)
