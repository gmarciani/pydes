import unittest

from pydes.core.utils.csv_utils import str_csv
from pydes.core.utils.report import PART, WIDTH, SimpleReport


class ReportTest(unittest.TestCase):
    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.r = SimpleReport("SAMPLE REPORT")
        self.sections = [
            ("Section-1", [("1st Value", 1), ("2nd Value", 2.123), ("3rd Value", "Hello World")]),
            (
                "Section-2/Subsection-1",
                [("1st Value", 1), ("2nd Value", 2.123), ("3rd Value", "Hello World")],
            ),
            ("Section-3", [("1st Value", 1), ("2nd Value", 2.123), ("3rd Value", "Hello World")]),
        ]
        for section_title, params in self.sections:
            for param_title, param_value in params:
                self.r.add(section_title, param_title, param_value)

        self.file_txt = "test.txt"
        self.file_csv = "test.csv"

    def _expected_str(self):
        title_separator = "=" * WIDTH
        fmt_title = "\n{}\n{:^" + str(WIDTH) + "}\n{}\n"
        fmt_section = "\n{:^" + str(WIDTH) + "}\n"
        fmt_value = "{:.<" + str(int(PART * WIDTH)) + "}{:.>" + str(int((1.0 - PART) * WIDTH)) + "}\n"

        s = fmt_title.format(title_separator, self.r.title, title_separator)
        for section_title, params in self.sections:
            s += fmt_section.format(section_title)
            for param_title, param_value in params:
                s += fmt_value.format(param_title, str(param_value))
        return s

    def test_string_representation(self):
        """
        Test the report string representation.
        :return: None
        """
        self.assertEqual(self._expected_str(), str(self.r), "String representation is not correct.")

    def test_save_txt(self):
        """
        Test the report saving to a TXT file.
        :return: None
        """
        self.r.save_txt(self.file_txt)

        with open(self.file_txt, "r") as f:
            actual = f.read()

        self.assertEqual(self._expected_str(), actual, "TXT file representation is not correct.")

    def test_save_txt_empty_clears_existing_content_first(self):
        with open(self.file_txt, "w") as f:
            f.write("stale content")

        self.r.save_txt(self.file_txt, empty=True)

        with open(self.file_txt, "r") as f:
            actual = f.read()

        self.assertEqual(self._expected_str(), actual, "TXT file representation is not correct.")

    def test_save_csv(self):
        """
        Test the report saving to a CSV file.
        :return: None
        """
        header = ["name"]
        row = ["SAMPLE REPORT"]
        for section_title, params in self.sections:
            for param_title, param_value in params:
                header.append(str_csv("{}_{}".format(section_title, param_title)))
                row.append(str(param_value))

        expected = "{}\n{}\n".format(",".join(header), ",".join(row))

        self.r.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(expected, actual, "CSV file representation is not correct.")

    def test_get_returns_value_when_present(self):
        self.assertEqual(1, self.r.get("Section-1", "1st Value"))
        self.assertEqual(2.123, self.r.get("Section-1", "2nd Value"))

    def test_get_returns_none_when_param_missing(self):
        self.assertIsNone(self.r.get("Section-1", "Missing Value"))

    def test_add_all(self):
        class Sample:
            def __init__(self):
                self.count = 3
                self.ratio = 1.23456789012
                self.label = "hello"
                self._hidden = "should be skipped"

            def method(self):
                return None

        r = SimpleReport("ADD ALL REPORT")
        r.add_all("Section", Sample())

        self.assertEqual("3", r.get("Section", "count"))
        self.assertEqual(round(1.23456789012, 10), r.get("Section", "ratio"))
        self.assertEqual("hello", r.get("Section", "label"))
        self.assertIsNone(r.get("Section", "_hidden"))
        self.assertIsNone(r.get("Section", "method"))

    def test_add_all_attrs(self):
        class Sample:
            def __init__(self):
                self.count = 3
                self.ratio = 1.23456789012
                self.label = "hello"

            def method(self):
                return None

        r = SimpleReport("ADD ALL ATTRS REPORT")
        r.add_all_attrs("Section", Sample(), "count", "ratio", "method", "missing")

        self.assertEqual(3, r.get("Section", "count"))
        self.assertEqual(round(1.23456789012, 10), r.get("Section", "ratio"))
        self.assertIsNone(r.get("Section", "method"))
        self.assertIsNone(r.get("Section", "missing"))


if __name__ == "__main__":
    unittest.main()
