"""Module that contains the converters utils unittests."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend.utils.converters import str_to_bool


class TestConvertersUtils(BaseTestCase):
    """Unit tests for the converters utils."""

    def test_str_to_bool(self):
        """Tests the str_to_bool function."""
        truthy_strs = ["true", "t", "yes", "1", "enabled", "on"]
        falsy_strs = ["false", "f", "no", "0", "disabled", "off"]

        for truthy_str in truthy_strs:
            with self.subTest(val=truthy_str):
                bool_value = str_to_bool(truthy_str)
                self.assertIsInstance(bool_value, bool)
                self.assertEqual(bool_value, True)

        for falsy_str in falsy_strs:
            with self.subTest(val=falsy_str):
                bool_value = str_to_bool(falsy_str)
                self.assertIsInstance(bool_value, bool)
                self.assertEqual(bool_value, False)

    def test_str_to_bool_invalid(self):
        """Tests the str_to_bool function with invalid input."""
        invalid_inputs = ["maybe", True, 1, "Y", " ", "\n", None]
        for invalid_input in invalid_inputs:
            with self.subTest(val=invalid_input):
                with self.assertRaises(ValueError):
                    str_to_bool(invalid_input)


if __name__ == "__main__":
    unittest.main()
