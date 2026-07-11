import unittest

from pydes.core.rnd.rndgen import MarcianiMultiStream, MarcianiSingleStream


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

        generator = MarcianiSingleStream(modulus=MODULUS, multiplier=MULTIPLIER, iseed=SEED)
        for _ in range(0, CHECK_ITERS):
            generator.rnd()

        self.assertEqual(generator.get_seed(), CHECK_VALUE, "{} is not correct!".format(generator.__class__.__name__))

    def test_rnd_multi_stream(self):
        """
        Verify the correctness of the Lehmer rnd number generator: MarcianiMultiStream
        :return: None
        """
        MODULUS = 2147483647
        MULTIPLIER = 48271
        SEED = 1
        STREAMS = 128
        JUMPER = 40509

        CHECK_VALUE = 399268537
        CHECK_ITERS = 10000

        generator = MarcianiMultiStream(
            modulus=MODULUS, multiplier=MULTIPLIER, streams=STREAMS, jumper=JUMPER, iseed=SEED
        )
        for _ in range(0, CHECK_ITERS):
            generator.rnd()

        self.assertEqual(generator.get_seed(), CHECK_VALUE, "{} is not correct!".format(generator.__class__.__name__))

    def test_single_stream_getters(self):
        modulus = 2147483647
        multiplier = 48271
        seed = 1

        generator = MarcianiSingleStream(iseed=seed, modulus=modulus, multiplier=multiplier)

        self.assertEqual(generator.get_initial_seed(), seed)
        self.assertEqual(generator.get_modulus(), modulus)
        self.assertEqual(generator.get_multiplier(), multiplier)
        self.assertEqual(generator.get_seed(), seed)

    def test_single_stream_put_seed(self):
        generator = MarcianiSingleStream(iseed=1)

        generator.put_seed(999)

        self.assertEqual(generator.get_seed(), 999)

    def test_single_stream_put_seed_raises_on_non_positive(self):
        generator = MarcianiSingleStream(iseed=1)

        with self.assertRaises(ValueError):
            generator.put_seed(0)

        with self.assertRaises(ValueError):
            generator.put_seed(-5)

    def test_single_stream_put_seed_wraps_modulus(self):
        modulus = 2147483647
        generator = MarcianiSingleStream(iseed=1, modulus=modulus)

        generator.put_seed(modulus + 10)

        self.assertEqual(generator.get_seed(), 10)

    def test_multi_stream_getters(self):
        modulus = 2147483647
        multiplier = 48271
        streams = 128
        jumper = 40509
        seed = 1

        generator = MarcianiMultiStream(
            iseed=seed, modulus=modulus, multiplier=multiplier, streams=streams, jumper=jumper
        )

        self.assertEqual(generator.get_initial_seed(), seed)
        self.assertEqual(generator.get_modulus(), modulus)
        self.assertEqual(generator.get_multiplier(), multiplier)
        self.assertEqual(generator.get_nstreams(), streams)
        self.assertEqual(generator.get_jumper(), jumper)

    def test_multi_stream_put_seed(self):
        generator = MarcianiMultiStream(iseed=1)

        generator.put_seed(12345)

        self.assertEqual(generator.get_seed(), 12345)

    def test_multi_stream_put_seed_raises_on_non_positive(self):
        generator = MarcianiMultiStream(iseed=1)

        with self.assertRaises(ValueError):
            generator.put_seed(0)

        with self.assertRaises(ValueError):
            generator.put_seed(-1)

    def test_multi_stream_put_seed_wraps_modulus(self):
        modulus = 2147483647
        generator = MarcianiMultiStream(iseed=1, modulus=modulus)

        generator.put_seed(modulus + 7)

        self.assertEqual(generator.get_seed(), 7)

    def test_multi_stream_stream_selection_is_disjoint(self):
        generator = MarcianiMultiStream(iseed=1)

        generator.stream(0)
        seed0 = generator.get_seed()
        generator.stream(3)
        seed3 = generator.get_seed()

        self.assertNotEqual(seed0, seed3)

        # Selecting a stream index beyond the range wraps around (modulo).
        generator.stream(generator.get_nstreams() + 3)
        wrapped_seed = generator.get_seed()
        self.assertEqual(wrapped_seed, seed3)

    def test_multi_stream_stream_lazily_plants_seeds_when_uninitialized(self):
        generator = MarcianiMultiStream(iseed=1)

        generator.stream(5)
        expected_seed = generator.get_seed()

        # Force the lazy re-planting branch inside stream(): _init False and
        # a non-zero requested stream triggers a call to plant_seeds().
        generator._init = False
        generator._seeds = [int(generator.get_initial_seed())] * generator.get_nstreams()
        generator.stream(5)

        self.assertEqual(generator.get_seed(), expected_seed)
        self.assertTrue(generator._init)


if __name__ == "__main__":
    unittest.main()
