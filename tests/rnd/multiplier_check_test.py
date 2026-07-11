import unittest

from pydes.core.rnd.inspection import multiplier_check


class MultiplierCheckTest(unittest.TestCase):
    """
    All tests use small prime moduli so is_fp_multiplier/is_mc_multiplier
    (which assume a prime modulus) run near-instantly and terminate.
    """

    def test_is_fp_multiplier_true_and_false(self):
        MODULUS = 11
        self.assertTrue(multiplier_check.is_fp_multiplier(2, MODULUS))
        self.assertFalse(multiplier_check.is_fp_multiplier(3, MODULUS))

    def test_is_mc_multiplier_true_and_false(self):
        MODULUS = 11
        self.assertTrue(multiplier_check.is_mc_multiplier(2, MODULUS))
        self.assertFalse(multiplier_check.is_mc_multiplier(4, MODULUS))

    def test_get_first_fp_multiplier(self):
        MODULUS = 11
        self.assertEqual(multiplier_check.get_first_fp_multiplier(MODULUS), 2)

    def test_get_first_fp_multiplier_none_when_search_space_empty(self):
        # modulus == 1 makes range(1, modulus) empty, so no candidate is checked.
        self.assertIsNone(multiplier_check.get_first_fp_multiplier(1))

    def test_get_fp_multipliers(self):
        MODULUS = 11
        fp_multipliers = multiplier_check.get_fp_multipliers(MODULUS)

        self.assertEqual(sorted(fp_multipliers), [2, 6, 7, 8])
        for multiplier in fp_multipliers:
            self.assertTrue(multiplier_check.is_fp_multiplier(multiplier, MODULUS))

    def test_get_fp_multipliers_first_fpm_equal_one(self):
        # modulus == 2 makes 1 the first (and only) FP multiplier, exercising
        # the "if first_fpm == 1" branch.
        fp_multipliers = multiplier_check.get_fp_multipliers(2)

        self.assertEqual(fp_multipliers, [1])

    def test_get_fp_multipliers_empty_when_no_first_fpm(self):
        self.assertEqual(multiplier_check.get_fp_multipliers(1), [])

    def test_get_mc_multipliers(self):
        MODULUS = 11
        mc_multipliers = multiplier_check.get_mc_multipliers(MODULUS)

        self.assertEqual(mc_multipliers, [1, 2, 3, 5])
        for multiplier in mc_multipliers:
            self.assertTrue(multiplier_check.is_mc_multiplier(multiplier, MODULUS))

    def test_generate_fp_multipliers(self):
        MODULUS = 11
        first_fpm = multiplier_check.get_first_fp_multiplier(MODULUS)

        fp_multipliers = multiplier_check.generate_fp_multipliers(first_fpm, MODULUS)

        self.assertEqual(sorted(fp_multipliers), sorted(multiplier_check.get_fp_multipliers(MODULUS)))

    def test_generate_fpmc_multipliers(self):
        MODULUS = 11
        first_fpm = multiplier_check.get_first_fp_multiplier(MODULUS)

        multipliers = multiplier_check.generate_fpmc_multipliers(first_fpm, MODULUS)

        self.assertTrue(len(multipliers) > 0)
        for multiplier in multipliers:
            self.assertTrue(0 < multiplier < MODULUS)

    def test_module_self_test_passes(self):
        # Exercises the module's own _test() sanity check, which cross-checks
        # get_fp_multipliers/is_fp_multiplier/is_mc_multiplier against known
        # results for a handful of small prime moduli.
        multiplier_check._test()


if __name__ == "__main__":
    unittest.main()
