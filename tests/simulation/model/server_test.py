import unittest
from types import SimpleNamespace

from pydes.core.simulation.model.server import SimpleServer


class SimpleServerTest(unittest.TestCase):
    def setUp(self):
        self.server = SimpleServer(SimpleNamespace(str={}), 0)

    def test_str(self):
        """
        Verify the string representation does not raise and contains useful info.
        :return: None
        """
        self.assertIn("Server(", str(self.server))

    def test_eq_with_non_server_returns_false(self):
        """
        Verify that comparing a server with a non-server object is always False.
        :return: None
        """
        self.assertFalse(self.server == "not-a-server")

    def test_eq_with_itself(self):
        """
        Verify identity-based equality.
        :return: None
        """
        self.assertEqual(self.server, self.server)

    def test_eq_with_a_different_server_instance(self):
        """
        Verify that two distinct server instances are not equal, even with identical state.
        :return: None
        """
        other = SimpleServer(SimpleNamespace(str={}), 0)
        self.assertNotEqual(self.server, other)


if __name__ == "__main__":
    unittest.main()
