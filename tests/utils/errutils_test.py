import unittest

from pydes.core.utils.errutils import error_one_tail, error_two_tails


class ErrUtilsTest(unittest.TestCase):
    def setUp(self):
        self.data = [(i, i) for i in range(1, 11)]

    def test_error_two_tails(self):
        error = error_two_tails(self.data, mn=2, mx=8, confidence=0.8)

        self.assertEqual(2, error["err_thr"])
        self.assertAlmostEqual(0.2, error["err_thr_perc"])
        self.assertEqual(1, error["err_mn"])
        self.assertEqual(2, error["err_mx"])
        self.assertEqual(3, error["err_emp"])
        self.assertAlmostEqual(0.1, error["err_mn_perc"])
        self.assertAlmostEqual(0.2, error["err_mx_perc"])
        self.assertAlmostEqual(0.3, error["err_emp_perc"])
        self.assertAlmostEqual(0.5, error["err_emp_thr_perc"])

    def test_error_one_tail(self):
        error = error_one_tail(self.data, mx=8, confidence=0.8)

        self.assertEqual(2, error["err_thr"])
        self.assertAlmostEqual(0.2, error["err_thr_perc"])
        self.assertEqual(2, error["err_mx"])
        self.assertEqual(2, error["err_emp"])
        self.assertAlmostEqual(0.2, error["err_mx_perc"])
        self.assertAlmostEqual(0.2, error["err_emp_perc"])
        self.assertAlmostEqual(0.0, error["err_emp_thr_perc"])

    def test_error_two_tails_no_errors(self):
        error = error_two_tails(self.data, mn=0, mx=11, confidence=0.5)

        self.assertEqual(0, error["err_mn"])
        self.assertEqual(0, error["err_mx"])
        self.assertEqual(0, error["err_emp"])


if __name__ == "__main__":
    unittest.main()
