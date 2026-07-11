import os
import shutil
import tempfile
import unittest

from pydes.core.utils.file_utils import (
    append_csv,
    append_list_of_numbers,
    append_list_of_pairs,
    create_dir_tree,
    empty_file,
    exists_file,
    is_empty_file,
    save_csv,
    save_header_csv,
    save_list_of_numbers,
    save_list_of_pairs,
    save_txt,
)


class FileUtilsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="pydes-file-utils-test-")
        self.filename = os.path.join(self.tmpdir, "sub", "data.txt")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_exists_file_with_dirname(self):
        self.assertFalse(exists_file(self.filename))
        create_dir_tree(self.filename)
        with open(self.filename, "w"):
            pass
        self.assertTrue(exists_file(self.filename))

    def test_exists_file_without_dirname(self):
        cwd = os.getcwd()
        os.chdir(self.tmpdir)
        try:
            self.assertFalse(exists_file("plain.txt"))
            with open("plain.txt", "w"):
                pass
            self.assertTrue(exists_file("plain.txt"))
        finally:
            os.chdir(cwd)

    def test_create_dir_tree(self):
        create_dir_tree(self.filename)
        self.assertTrue(os.path.isdir(os.path.dirname(self.filename)))

    def test_empty_file_creates_directory_and_empty_file(self):
        empty_file(self.filename)
        self.assertTrue(os.path.exists(self.filename))
        self.assertTrue(is_empty_file(self.filename))

    def test_is_empty_file_false_when_content_present(self):
        create_dir_tree(self.filename)
        with open(self.filename, "w") as f:
            f.write("hello")
        self.assertFalse(is_empty_file(self.filename))

    def test_empty_file_clears_existing_content(self):
        create_dir_tree(self.filename)
        with open(self.filename, "w") as f:
            f.write("hello")
        empty_file(self.filename)
        self.assertTrue(is_empty_file(self.filename))

    def test_save_list_of_numbers(self):
        save_list_of_numbers(self.filename, [1, 2, 3])
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("1\n2\n3\n", content)

    def test_append_list_of_numbers(self):
        save_list_of_numbers(self.filename, [1, 2])
        append_list_of_numbers(self.filename, [3])
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("1\n2\n3\n", content)

    def test_save_list_of_pairs(self):
        save_list_of_pairs(self.filename, [(1, 2), (3, 4)])
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("1,2\n3,4\n", content)

    def test_append_list_of_pairs(self):
        save_list_of_pairs(self.filename, [(1, 2)])
        append_list_of_pairs(self.filename, [(3, 4)])
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("1,2\n3,4\n", content)

    def test_save_header_and_append_csv(self):
        list_dict = {"a": "1", "b": "2"}
        save_header_csv(self.filename, list_dict)
        append_csv(self.filename, list_dict)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("a,b\n1,2\n", content)

    def test_save_csv(self):
        list_dict = {"a": "1", "b": "2"}
        save_csv(self.filename, list_dict)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("a,b\n1,2\n", content)

    def test_save_txt_default(self):
        save_txt("hello", self.filename)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("hello", content)

    def test_save_txt_append(self):
        save_txt("hello", self.filename)
        save_txt(" world", self.filename, append=True)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("hello world", content)

    def test_save_txt_empty_before_writing(self):
        save_txt("hello", self.filename)
        save_txt("world", self.filename, empty=True)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("world", content)

    def test_save_txt_non_string_content(self):
        save_txt(123, self.filename)
        with open(self.filename, "r") as f:
            content = f.read()
        self.assertEqual("123", content)


if __name__ == "__main__":
    unittest.main()
