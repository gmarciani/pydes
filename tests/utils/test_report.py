import unittest
from core.utils.report import SimpleReport


class ReportTest(unittest.TestCase):

    def setUp(self):
        """
        The test setup.
        :return: None
        """
        self.r = SimpleReport("SAMPLE REPORT")
        self.r.add("Section-1", "1st Value", 1)
        self.r.add("Section-1", "2nd Value", 2.123)
        self.r.add("Section-1", "3rd Value", "Hello World")
        self.r.add("Section-2/Subsection-1", "1st Value", 1)
        self.r.add("Section-2/Subsection-1", "2nd Value", 2.123)
        self.r.add("Section-2/Subsection-1", "3rd Value", "Hello World")
        self.r.add("Section-3", "1st Value", 1)
        self.r.add("Section-3", "2nd Value", 2.123)
        self.r.add("Section-3", "3rd Value", "Hello World")

        self.file_txt = "test.txt"
        self.file_csv = "test.csv"

    def test_string_representation(self):
        """
        Test the report string representation.
        :return: None
        """
        s = "\n"
        s += "==================================================\n"
        s += "                  SAMPLE REPORT                   \n"
        s += "==================================================\n"
        s += "\n"
        s += "                    Section-1                     \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"
        s += "\n"
        s += "              Section-2/Subsection-1              \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"
        s += "\n"
        s += "                    Section-3                     \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"

        self.assertEqual(s, str(self.r), "String representation is not correct.")

    def test_save_txt(self):
        """
        Test the report saving to a TXT file.
        :return: None
        """
        s = "\n"
        s += "==================================================\n"
        s += "                  SAMPLE REPORT                   \n"
        s += "==================================================\n"
        s += "\n"
        s += "                    Section-1                     \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"
        s += "\n"
        s += "              Section-2/Subsection-1              \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"
        s += "\n"
        s += "                    Section-3                     \n"
        s += "1st Value........................................1\n"
        s += "2nd Value....................................2.123\n"
        s += "3rd Value..............................Hello World\n"

        self.r.save(self.file_txt)

        with open(self.file_txt, "r") as f:
            actual = f.read()

        self.assertEqual(s, actual, "TXT file representation is not correct.")

    def test_save_csv(self):
        """
        Test the report saving to a CSV file.
        :return: None
        """
        s = "name,section-1.1st_value,section-1.2nd_value,section-1.3rd_value,section-2/subsection-1.1st_value,section-2/subsection-1.2nd_value,section-2/subsection-1.3rd_value,section-3.1st_value,section-3.2nd_value,section-3.3rd_value,\n"
        s += "SAMPLE REPORT,1,2.123,Hello World,1,2.123,Hello World,1,2.123,Hello World,\n"

        self.r.save_csv(self.file_csv)

        with open(self.file_csv, "r") as f:
            actual = f.read()

        self.assertEqual(s, actual, "CSV file representation is not correct.")


if __name__ == "__main__":
    unittest.main()
