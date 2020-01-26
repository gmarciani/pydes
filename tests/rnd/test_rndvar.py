import unittest
from core.rnd.rndgen import MarcianiMultiStream
from core.rnd.rndcmp import RandomComponent
from core.rnd.rndvar import Variate
from statistics import mean, variance
from math import exp


class RndvarTest(unittest.TestCase):

    def setUp(self):
        """
        Set up the test.
        :return: None.
        """
        self.rndgen = MarcianiMultiStream()
        self.samsize = 10000
        self.err = 0.05
        self.makeAssertion = False

        self.varparams = {
            Variate.BERNOULLI: dict(p=0.8),
            Variate.BINOMIAL: dict(n=5, p=0.8),
            Variate.CHISQUARE: dict(n=5),
            Variate.EQUILIKELY: dict(a=10.0, b=20.0),
            Variate.ERLANG: dict(n=5, b=0.8),
            Variate.EXPONENTIAL: dict(m=0.8),
            Variate.GEOMETRIC: dict(p=0.8),
            Variate.LOGNORMAL: dict(a=5, b=0.8),
            Variate.NORMAL: dict(m=1.0, s=0.5),
            Variate.PASCAL: dict(n=5, p=0.8),
            Variate.POISSON: dict(m=5),
            Variate.STUDENT: dict(n=5),
            Variate.UNIFORM: dict(a=10.0, b=20.0)
        }

        self.check_mean = {
            Variate.BERNOULLI: lambda p: p,
            Variate.BINOMIAL: lambda n, p: n * p,
            Variate.CHISQUARE: lambda n: n,
            Variate.EQUILIKELY: lambda a, b: (a + b) / 2.0,
            Variate.ERLANG: lambda n, b: n * b,
            Variate.EXPONENTIAL: lambda m: m,
            Variate.GEOMETRIC: lambda p: p / (1.0 - p),
            Variate.LOGNORMAL: lambda a, b: exp(a + 0.5 * b * b),
            Variate.NORMAL: lambda m, s: m,
            Variate.PASCAL: lambda n, p: n * p / (1.0 - p),
            Variate.POISSON: lambda m: m,
            Variate.STUDENT: lambda n: 0.0,
            Variate.UNIFORM: lambda a, b: (a + b) / 2.0
        }

        self.check_variance = {
            Variate.BERNOULLI: lambda p: p * (1.0 - p),
            Variate.BINOMIAL: lambda n, p: n * p * (1.0 - p),
            Variate.CHISQUARE: lambda n: 2.0 * n,
            Variate.EQUILIKELY: lambda a, b: (pow(b - a + 1.0, 2) - 1.0) / 12.0,
            Variate.ERLANG: lambda n, b: n * b * b,
            Variate.EXPONENTIAL: lambda m: pow(m, 2.0),
            Variate.GEOMETRIC: lambda p: p / pow(1.0 - p, 2.0),
            Variate.LOGNORMAL: lambda a, b: exp(b * b) - exp(2.0 * a + b * b),
            Variate.NORMAL: lambda m, s: s * s,
            Variate.PASCAL: lambda n, p: n * p / ((1.0 - p) * (1.0 - p)),
            Variate.POISSON: lambda m: m,
            Variate.STUDENT: lambda n: n / (n - 2.0),
            Variate.UNIFORM: lambda a, b: pow(b - a, 2.0) / 12.0
        }

    def test_parametric_variates(self):
        """
        Verify the correctness of the rnd variates generation.
        :return: None
        """
        for variate in Variate:
            params = self.varparams[variate]
            sample = list()
            for i in range(self.samsize):
                rndvalue = Variate[variate.name].vargen.generate(u=self.rndgen, **params)
                sample.append(rndvalue)

            expected_mean = self.check_mean[variate](**params)
            actual_mean = mean(sample)
            print("{}: expected mean {}, got {}".format(variate.name, expected_mean, actual_mean))

            if self.makeAssertion:
                self.assertLessEqual(abs(expected_mean - actual_mean) / expected_mean,
                                     self.err * expected_mean,
                                     "Mean error for variate {}: expected {} got {}"
                                     .format(variate.name, expected_mean, actual_mean))

            expected_variance = self.check_variance[variate](**params)
            actual_variance = variance(sample)
            print("{}: expected variance {}, got {}".format(variate.name, expected_variance, actual_variance))

            if self.makeAssertion:
                self.assertLessEqual(abs(expected_variance - actual_variance) / expected_variance,
                                     self.err * expected_variance,
                                     "Variance error for variate {}: expected {} got {}"
                                     .format(variate.name, expected_variance, actual_variance))

if __name__ == "__main__":
    unittest.main()
