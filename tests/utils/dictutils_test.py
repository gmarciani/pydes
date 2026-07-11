import unittest

from pydes.core.utils.dictutils import merge


class DictUtilsTest(unittest.TestCase):
    def test_merge_adds_new_keys(self):
        a = {"a": 1}
        b = {"b": 2}
        result = merge(a, b)
        self.assertEqual({"a": 1, "b": 2}, result)

    def test_merge_overwrites_non_dict_values(self):
        a = {"a": 1, "b": 2}
        b = {"b": 3}
        result = merge(a, b)
        self.assertEqual({"a": 1, "b": 3}, result)

    def test_merge_recurses_into_nested_dicts(self):
        a = {"a": "1", "b": {"c": "2", "d": "3"}}
        b = {"b": {"d": "5"}}
        result = merge(a, b)
        self.assertEqual({"a": "1", "b": {"c": "2", "d": "5"}}, result)

    def test_merge_mutates_and_returns_first_argument(self):
        a = {"a": {"x": 1}}
        b = {"a": {"y": 2}}
        result = merge(a, b)
        self.assertIs(a, result)
        self.assertEqual({"a": {"x": 1, "y": 2}}, a)

    def test_merge_replaces_dict_with_non_dict(self):
        a = {"a": {"x": 1}}
        b = {"a": 5}
        result = merge(a, b)
        self.assertEqual({"a": 5}, result)


if __name__ == "__main__":
    unittest.main()
