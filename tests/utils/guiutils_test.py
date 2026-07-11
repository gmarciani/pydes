import contextlib
import io
import unittest

from pydes.core.utils.guiutils import get_splash, print_progress


class GuiUtilsTest(unittest.TestCase):
    def test_get_splash(self):
        splash = get_splash()
        self.assertIsInstance(splash, str)
        self.assertGreater(len(splash), 0)

    def test_print_progress_start(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_progress(0, 100)
        output = buf.getvalue()
        self.assertIn("PROGRESS", output)
        self.assertIn("0%", output)
        self.assertIn("(0/100)", output)

    def test_print_progress_middle(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_progress(50, 100)
        output = buf.getvalue()
        self.assertIn("50%", output)
        self.assertIn("(50/100)", output)

    def test_print_progress_complete(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_progress(100, 100, message="done")
        output = buf.getvalue()
        self.assertIn("100%", output)
        self.assertIn("(100/100)", output)
        self.assertIn("{ done }", output)

    def test_print_progress_no_message(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            print_progress(1, 4)
        output = buf.getvalue()
        self.assertIn("{ no message }", output)


if __name__ == "__main__":
    unittest.main()
