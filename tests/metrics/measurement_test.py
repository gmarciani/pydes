import unittest

from pydes.core.metrics.measurement import Measure


class MeasurementTest(unittest.TestCase):
    def test_default_value_and_unit(self):
        measure = Measure()
        self.assertEqual(0.0, measure.get_value())
        self.assertIsNone(measure.get_unit())

    def test_unit(self):
        measure = Measure(unit="ms")
        self.assertEqual("ms", measure.get_unit())

    def test_set_value(self):
        measure = Measure()
        measure.set_value(42)
        self.assertEqual(42, measure.get_value())

    def test_str_and_repr(self):
        measure = Measure(unit="ms")
        measure.set_value(5)

        s = str(measure)
        r = repr(measure)

        self.assertEqual(s, r)
        self.assertIn("SampleMeasure(", s)
        self.assertIn("_value=5", s)
        self.assertIn("_unit=ms", s)


if __name__ == "__main__":
    unittest.main()
