import unittest
from core.random.rndgen import MarcianiMultiStream
from core.random.rndvar import Variate
from statistics import mean, variance


class RndvarTest(unittest.TestCase):

    def setUp(self):
        """
        Set up the test.
        :return: None.
        """
        self.rndgen = MarcianiMultiStream()
        self.samsize = 100000
        self.err = 0.01
        self.makeAssertion = True

    def test_parametric_variates(self):
        """
        Verify the correctness of the random variates generation.
        :return: None
        """
        rndgen = MarcianiMultiStream()
        varparams = {
            Variate.EQUILIKELY: dict(a=10.0, b=20.0),
            Variate.EXPONENTIAL: dict(m=0.8),
            Variate.GEOMETRIC: dict(p=0.8),
            Variate.UNIFORM: dict(a=10.0, b= 20.0)
        }

        check_mean = {
            Variate.EQUILIKELY: lambda a, b: (a + b) / 2,
            Variate.EXPONENTIAL: lambda m: m,
            Variate.GEOMETRIC: lambda p: p / (1 - p),
            Variate.UNIFORM: lambda a, b: (a + b) / 2
        }

        check_variance = {
            Variate.EQUILIKELY: lambda a, b: (pow(b - a + 1, 2) - 1) / 12,
            Variate.EXPONENTIAL: lambda m: pow(m, 2),
            Variate.GEOMETRIC: lambda p: p / pow(1 - p, 2),
            Variate.UNIFORM: lambda a, b: pow(b - a, 2) / 12
        }

        for variate in Variate:
            params = varparams[variate]
            sample = list()
            for i in range(self.samsize):
                rndvalue = Variate[variate.name].vargen.generate(u=rndgen, **params)
                sample.append(rndvalue)

            expected_mean = check_mean[variate](**params)
            actual_mean = mean(sample)
            print("{}: expected mean {}, got {}".format(variate.name, expected_mean, actual_mean))

            if self.makeAssertion:
                self.assertLessEqual(abs(expected_mean - actual_mean) / expected_mean,
                                     self.err * expected_mean,
                                     "Mean error for variate {}: expected {} got {}"
                                     .format(variate.name, expected_mean, actual_mean))

            expected_variance = check_variance[variate](**params)
            actual_variance = variance(sample)
            print("{}: expected variance {}, got {}".format(variate.name, expected_variance, actual_variance))

            if self.makeAssertion:
                self.assertLessEqual(abs(expected_variance - actual_variance) / expected_variance,
                                     self.err * expected_variance,
                                     "Variance error for variate {}: expected {} got {}"
                                     .format(variate.name, expected_variance, actual_variance))

if __name__ == "__main__":
    unittest.main()
