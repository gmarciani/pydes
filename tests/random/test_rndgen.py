import unittest
from core.random.rndgen import MarcianiMultiStream


class RndgenTest(unittest.TestCase):

    def test_rnd_32bit(self):
        """
        Verify the correctness of the Lehmer random nunber generator.
        :return: None
        """
        CHECK_VALUE = 399268537
        CHECK_ITERS = 10000
        JUMPER = 22925

        ok = False

        generator = MarcianiMultiStream(1)

        #rndgen.select_stream(0)
        #rndgen.put_seed(1)
        for i in range(0, CHECK_ITERS):
            generator.rnd()
        x = generator.get_seed()
        ok = (x == CHECK_VALUE)

        generator.stream(1)
        generator.plant_seeds(1)
        x = generator.get_seed()
        ok = (ok is True) and (x == JUMPER)

        self.assertTrue(ok, "The implementation of rndgen (32bit) is not correct.")


if __name__ == "__main__":
    unittest.main()
