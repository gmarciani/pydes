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


if __name__ == "__main__":
    unittest.main()
