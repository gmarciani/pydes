import unittest
from core.rnd.rndgen import MarcianiSingleStream, MarcianiMultiStream


class RndgenTest(unittest.TestCase):

    def test_rnd_single_stream(self):
        """
        Verify the correctness of the Lehmer rnd number generator: MarcianiSingleStream
        :return: None
        """
        MODULUS = 2147483647
        MULTIPLIER = 48271
        SEED = 1

        CHECK_VALUE = 399268537
        CHECK_ITERS = 10000

        generator = MarcianiSingleStream(iseed=SEED)
        for _ in range(0, CHECK_ITERS):
            generator.rnd()
        if generator.get_seed() != CHECK_VALUE:
            raise RuntimeError("{} is not correct!".format(generator.__class__.__name__))

    def test_rnd_multi_stream(self):
        """
        Verify the correctness of the Lehmer rnd number generator: MarcianiMultiStream
        :return: None
        """
        MODULUS = 2147483647
        MULTIPLIER = 48271
        SEED = 1

        CHECK_VALUE = 399268537
        CHECK_ITERS = 10000

        generator = MarcianiMultiStream(iseed=SEED)
        for _ in range(0, CHECK_ITERS):
            generator.rnd()
        if generator.get_seed() != CHECK_VALUE:
            raise RuntimeError("{} is not correct!".format(generator.__class__.__name__))


if __name__ == "__main__":
    unittest.main()
