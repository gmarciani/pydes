import unittest
from math import comb, exp, lgamma, log

from pydes.core.rnd import rndf


class BernoulliTest(unittest.TestCase):
    def test_pdf(self):
        self.assertAlmostEqual(rndf.pdfBernoulli(0.3, 0), 0.7)
        self.assertAlmostEqual(rndf.pdfBernoulli(0.3, 1), 0.3)

    def test_cdf(self):
        self.assertAlmostEqual(rndf.cdfBernoulli(0.3, 0), 0.7)
        self.assertEqual(rndf.cdfBernoulli(0.3, 1), 1)

    def test_idf(self):
        self.assertEqual(rndf.idfBernoulli(0.3, 0.5), 0)
        self.assertEqual(rndf.idfBernoulli(0.3, 0.9), 1)
        self.assertEqual(rndf.idfBernoulli(0.3, 0.99), 1)


class EquilikelyTest(unittest.TestCase):
    def test_pdf_cdf(self):
        a, b = 1, 6
        for x in range(a, b + 1):
            self.assertAlmostEqual(rndf.pdfEquilikely(a, b, x), 1.0 / (b - a + 1.0))
            self.assertAlmostEqual(rndf.cdfEquilikely(a, b, x), (x - a + 1.0) / (b - a + 1.0))

    def test_idf_bounds(self):
        a, b = 1, 6
        self.assertEqual(rndf.idfEquilikely(a, b, 0.001), a)
        self.assertEqual(rndf.idfEquilikely(a, b, 0.999), b)

    def test_idf_roundtrip(self):
        a, b = 1, 6
        for x in range(a, b + 1):
            u = rndf.cdfEquilikely(a, b, x) - 1e-9
            self.assertEqual(rndf.idfEquilikely(a, b, u), x)


class BinomialTest(unittest.TestCase):
    def test_pdf_sums_to_one(self):
        n, p = 10, 0.5
        total = sum(rndf.pdfBinomial(n, p, x) for x in range(n + 1))
        self.assertAlmostEqual(total, 1.0, places=6)

    def test_pdf_x_zero_uses_logchoose_zero_branch(self):
        n, p = 10, 0.5
        self.assertAlmostEqual(rndf.pdfBinomial(n, p, 0), (1.0 - p) ** n)

    def test_cdf_at_n_is_one(self):
        n, p = 10, 0.4
        self.assertEqual(rndf.cdfBinomial(n, p, n), 1.0)

    def test_cdf_below_n(self):
        n, p = 10, 0.4
        expected = sum(rndf.pdfBinomial(n, p, x) for x in range(0, 4))
        self.assertAlmostEqual(rndf.cdfBinomial(n, p, 3), expected, places=6)

    def test_idf_roundtrip_all_branches(self):
        # Covers all three branches of idfBinomial: search upward from the
        # mean, search downward from the mean, and the x == 0 fallback.
        n, p = 10, 0.5
        for u in (0.0001, 0.001, 0.01, 0.5, 0.9, 0.99, 0.999):
            x = rndf.idfBinomial(n, p, u)
            hi = rndf.cdfBinomial(n, p, x)
            self.assertGreaterEqual(hi, u)
            if x > 0:
                lo = rndf.cdfBinomial(n, p, x - 1)
                self.assertLess(lo, u)


class GeometricTest(unittest.TestCase):
    def test_pdf_known_values(self):
        p = 0.6
        self.assertAlmostEqual(rndf.pdfGeometric(p, 0), 1.0 - p)
        self.assertAlmostEqual(rndf.pdfGeometric(p, 1), (1.0 - p) * p)

    def test_cdf_known_values(self):
        p = 0.6
        self.assertAlmostEqual(rndf.cdfGeometric(p, 0), 1.0 - p)

    def test_idf_roundtrip(self):
        p = 0.6
        for u in (0.1, 0.5, 0.9):
            x = rndf.idfGeometric(p, u)
            hi = rndf.cdfGeometric(p, x)
            self.assertGreaterEqual(hi, u)
            if x > 0:
                lo = rndf.cdfGeometric(p, x - 1)
                self.assertLess(lo, u)


class PascalTest(unittest.TestCase):
    def test_pdf_x_zero(self):
        n, p = 5, 0.4
        self.assertAlmostEqual(rndf.pdfPascal(n, p, 0), (1.0 - p) ** n)

    def test_idf_roundtrip_all_branches(self):
        n, p = 5, 0.4
        for u in (0.0001, 0.001, 0.1, 0.5, 0.9, 0.999):
            x = rndf.idfPascal(n, p, u)
            hi = rndf.cdfPascal(n, p, x)
            self.assertGreaterEqual(hi, u)
            if x > 0:
                lo = rndf.cdfPascal(n, p, x - 1)
                self.assertLess(lo, u)


class PoissonTest(unittest.TestCase):
    def test_pdf_known_value(self):
        m = 5.0
        self.assertAlmostEqual(rndf.pdfPoisson(m, 0), exp(-m))

    def test_idf_roundtrip_all_branches(self):
        m = 5.0
        for u in (0.0001, 0.001, 0.02, 0.5, 0.9, 0.999):
            x = rndf.idfPoisson(m, u)
            hi = rndf.cdfPoisson(m, x)
            self.assertGreaterEqual(hi, u)
            if x > 0:
                lo = rndf.cdfPoisson(m, x - 1)
                self.assertLess(lo, u)


class UniformTest(unittest.TestCase):
    def test_pdf(self):
        a, b = 2.0, 10.0
        self.assertAlmostEqual(rndf.pdfUniform(a, b, 5.0), 1.0 / (b - a))

    def test_idf_roundtrip(self):
        a, b = 2.0, 10.0
        for u in (0.1, 0.5, 0.9):
            x = rndf.idfUniform(a, b, u)
            self.assertAlmostEqual(rndf.cdfUniform(a, b, x), u)


class ExponentialTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        m = 3.0
        for u in (0.1, 0.5, 0.9):
            x = rndf.idfExponential(m, u)
            self.assertAlmostEqual(rndf.cdfExponential(m, x), u)
            self.assertGreater(rndf.pdfExponential(m, x), 0.0)


class ErlangTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        for n, b in ((3, 2.0), (1, 1.0), (10, 0.5)):
            for u in (0.05, 0.5, 0.95):
                x = rndf.idfErlang(n, b, u)
                self.assertAlmostEqual(rndf.cdfErlang(n, b, x), u, places=4)
                self.assertGreater(rndf.pdfErlang(n, b, x), 0.0)


class StandardNormalTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        for u in (0.01, 0.5, 0.99):
            x = rndf.idfStandard(u)
            self.assertAlmostEqual(rndf.cdfStandard(x), u, places=4)

    def test_cdf_symmetry(self):
        # Exercises both branches (x < 0.0 and x >= 0.0) of cdfStandard.
        self.assertAlmostEqual(rndf.cdfStandard(-1.0) + rndf.cdfStandard(1.0), 1.0, places=6)

    def test_pdf_symmetry(self):
        self.assertAlmostEqual(rndf.pdfStandard(-2.0), rndf.pdfStandard(2.0))

    def test_normal_idf_roundtrip(self):
        m, s = 5.0, 2.0
        for u in (0.1, 0.5, 0.9):
            x = rndf.idfNormal(m, s, u)
            self.assertAlmostEqual(rndf.cdfNormal(m, s, x), u, places=4)
            self.assertGreater(rndf.pdfNormal(m, s, x), 0.0)


class LognormalTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        a, b = 1.0, 0.5
        for u in (0.1, 0.5, 0.9):
            x = rndf.idfLognormal(a, b, u)
            self.assertAlmostEqual(rndf.cdfLognormal(a, b, x), u, places=4)
            self.assertGreater(rndf.pdfLognormal(a, b, x), 0.0)


class ChisquareTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        for n in (1, 5, 20):
            for u in (0.05, 0.5, 0.95):
                x = rndf.idfChisquare(n, u)
                self.assertAlmostEqual(rndf.cdfChisquare(n, x), u, places=4)
                self.assertGreater(rndf.pdfChisquare(n, x), 0.0)


class StudentTest(unittest.TestCase):
    def test_idf_roundtrip(self):
        for n in (1, 5, 30):
            for u in (0.05, 0.5, 0.95):
                x = rndf.idfStudent(n, u)
                self.assertAlmostEqual(rndf.cdfStudent(n, x), u, places=4)
                self.assertGreater(rndf.pdfStudent(n, x), 0.0)

    def test_cdf_sign_branches(self):
        # Exercises both branches (x >= 0.0 and x < 0.0) of cdfStudent.
        n = 5
        self.assertAlmostEqual(rndf.cdfStudent(n, 0.0) + rndf.cdfStudent(n, 0.0), 1.0)
        self.assertLess(rndf.cdfStudent(n, -1.0), 0.5)
        self.assertGreater(rndf.cdfStudent(n, 1.0), 0.5)


class SpecialFunctionsTest(unittest.TestCase):
    def test_log_factorial(self):
        self.assertAlmostEqual(rndf.LogFactorial(0), 0.0, places=8)
        self.assertAlmostEqual(rndf.LogFactorial(5), log(120), places=6)

    def test_log_gamma(self):
        self.assertAlmostEqual(rndf.LogGamma(1), lgamma(1), places=8)
        self.assertAlmostEqual(rndf.LogGamma(6), lgamma(6), places=6)

    def test_log_beta(self):
        self.assertAlmostEqual(rndf.LogBeta(2, 3), log(1.0 / 12.0), places=6)

    def test_log_choose(self):
        self.assertAlmostEqual(rndf.LogChoose(5, 2), log(comb(5, 2)), places=6)
        # m == 0 branch
        self.assertEqual(rndf.LogChoose(5, 0), 0.0)

    def test_in_gamma_series_branch(self):
        # x < a + 1 -> evaluated as an infinite series
        value = rndf.InGamma(5, 2)
        self.assertGreater(value, 0.0)
        self.assertLess(value, 1.0)

    def test_in_gamma_continued_fraction_branch(self):
        # x >= a + 1 -> evaluated as a continued fraction
        value = rndf.InGamma(5, 20)
        self.assertGreater(value, 0.99)
        self.assertLessEqual(value, 1.0)

    def test_in_gamma_zero_x(self):
        # x == 0.0 -> factor branch set to 0.0
        self.assertEqual(rndf.InGamma(5, 0), 0.0)

    def test_in_beta_swap_and_no_swap_branches(self):
        a, b = 2, 3
        # x below (a+1)/(a+b+1) -> no swap
        no_swap = rndf.InBeta(a, b, 0.1)
        # x above (a+1)/(a+b+1) -> swap x and (a, b)
        swap = rndf.InBeta(a, b, 0.9)
        self.assertGreater(no_swap, 0.0)
        self.assertLess(no_swap, 1.0)
        self.assertGreater(swap, no_swap)

    def test_in_beta_zero_x(self):
        self.assertEqual(rndf.InBeta(2, 3, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
