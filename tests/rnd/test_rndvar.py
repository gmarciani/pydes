import unittest
from math import exp
from statistics import mean, variance

from core.rnd.rndgen import MarcianiMultiStream
from core.rnd.rndvar import Variate


class RndvarTest(unittest.TestCase):
    def setUp(self):
        """
        Set up the test.
        :return: None.
        """
        self.rndgen = MarcianiMultiStream()
        self.samsize = 50000
        self.err = 0.015

        self.varparams = {
            Variate.DETERMINISTIC: dict(v=0.9),
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
            Variate.UNIFORM: dict(a=10.0, b=20.0),
        }

        self.check_mean = {
            Variate.DETERMINISTIC: lambda v: v,
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
            Variate.UNIFORM: lambda a, b: (a + b) / 2.0,
        }

        self.check_variance = {
            Variate.DETERMINISTIC: lambda v: 0,
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
            Variate.UNIFORM: lambda a, b: pow(b - a, 2.0) / 12.0,
        }

    def test_bernoulli(self):
        self.__execute_test_on_variate(Variate.BERNOULLI)

    def test_binomial(self):
        self.__execute_test_on_variate(Variate.BINOMIAL)

    def test_chisquare(self):
        self.__execute_test_on_variate(Variate.CHISQUARE)

    def test_deterministic(self):
        self.__execute_test_on_variate(Variate.DETERMINISTIC)

    def test_equilikely(self):
        self.__execute_test_on_variate(Variate.EQUILIKELY)

    def test_erlang(self):
        self.__execute_test_on_variate(Variate.ERLANG)

    def test_exponential(self):
        self.__execute_test_on_variate(Variate.EXPONENTIAL)

    def test_geometric(self):
        self.__execute_test_on_variate(Variate.GEOMETRIC)

    def test_lognormal(self):
        self.__execute_test_on_variate(Variate.LOGNORMAL)

    def test_normal(self):
        self.__execute_test_on_variate(Variate.NORMAL)

    def test_pascal(self):
        self.__execute_test_on_variate(Variate.PASCAL)

    def test_poisson(self):
        self.__execute_test_on_variate(Variate.POISSON)

    def test_student(self):
        self.__execute_test_on_variate(Variate.STUDENT)

    def test_uniform(self):
        self.__execute_test_on_variate(Variate.UNIFORM)

    def __execute_test_on_variate(self, variate):
        """
        Verify the correctness of the rnd variates generation.
        :return: None
        """
        params = self.varparams[variate]
        sample = list()
        for i in range(self.samsize):
            rndvalue = Variate[variate.name].generator.generate(u=self.rndgen, **params)
            sample.append(rndvalue)

        expected_mean = self.check_mean[variate](**params)
        actual_mean = mean(sample)
        actual_mean_error = (
            abs(actual_mean - expected_mean) / expected_mean if expected_mean != 0 else abs(actual_mean - expected_mean)
        )

        expected_variance = self.check_variance[variate](**params)
        actual_variance = variance(sample)
        actual_variance_error = (
            abs(actual_variance - expected_variance) / expected_variance
            if expected_variance != 0
            else abs(actual_variance - expected_variance)
        )

        self.assertLessEqual(actual_mean_error, self.err)
        self.assertLessEqual(actual_variance_error, self.err)


if __name__ == "__main__":
    unittest.main()
