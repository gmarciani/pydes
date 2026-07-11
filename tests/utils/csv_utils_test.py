import os
import shutil
import tempfile
import unittest

from pydes.core.utils.csv_utils import read_csv, save_csv, str_csv


class CsvUtilsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="pydes-csv-utils-test-")
        self.filename = os.path.join(self.tmpdir, "sub", "data.csv")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_str_csv_replaces_spaces_and_slashes_and_lowers(self):
        self.assertEqual("a_b_c", str_csv("A B/C"))

    def test_save_csv_writes_header_and_rows(self):
        save_csv(self.filename, ["a", "b"], [(1, 2), (3, 4)])

        with open(self.filename, "r") as f:
            content = f.read()

        self.assertEqual("a,b\n1,2\n3,4\n", content)

    def test_save_csv_skip_header(self):
        save_csv(self.filename, ["a", "b"], [(1, 2)], skip_header=True)

        with open(self.filename, "r") as f:
            content = f.read()

        self.assertEqual("1,2\n", content)

    def test_save_csv_append(self):
        save_csv(self.filename, ["a", "b"], [(1, 2)])
        save_csv(self.filename, ["a", "b"], [(3, 4)], append=True, skip_header=True)

        with open(self.filename, "r") as f:
            content = f.read()

        self.assertEqual("a,b\n1,2\n3,4\n", content)

    def test_save_csv_empty_flag_clears_file_before_writing(self):
        save_csv(self.filename, ["a", "b"], [(1, 2)])
        save_csv(self.filename, ["a", "b"], [(3, 4)], empty=True)

        with open(self.filename, "r") as f:
            content = f.read()

        self.assertEqual("a,b\n3,4\n", content)

    def test_read_csv_roundtrip(self):
        save_csv(self.filename, ["a", "b"], [(1, 2), (3, 4)])

        result = read_csv(self.filename)

        self.assertEqual([{"a": "1", "b": "2"}, {"a": "3", "b": "4"}], result)


if __name__ == "__main__":
    unittest.main()
