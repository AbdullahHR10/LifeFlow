"""Module that contains the enums unittests."""

import unittest
from backend.utils.enums import BackgroundColor, Priority, Category, Frequency


class TestEnums(unittest.TestCase):
    """Unit tests for the enums."""
    def test_background_color_enum(self):
        """Tests BackgroundColor enum."""
        expected = {
            "BLUE": "Blue",
            "RED": "Red",
            "GREEN": "Green",
            "CYAN": "Cyan",
            "YELLOW": "Yellow",
            "ORANGE": "Orange",
            "PURPLE": "Purple",
        }
        for name, value in expected.items():
            with self.subTest(enum="BackgroundColor", name=name):
                self.assertEqual(getattr(BackgroundColor, name).value, value)
                self.assertEqual(BackgroundColor(value), getattr(
                    BackgroundColor, name))

    def test_priority_enum(self):
        """Tests Priority enum."""
        expected = {
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Critical",
        }
        for name, value in expected.items():
            with self.subTest(enum="Priority", name=name):
                self.assertEqual(getattr(Priority, name).value, value)
                self.assertEqual(Priority(value), getattr(Priority, name))

    def test_category_enum(self):
        """Tests Category enum."""
        expected = {
            "WORK": "Work",
            "PERSONAL": "Personal",
            "STUDY": "Study",
            "HEALTH": "Health",
            "HOBBY": "Hobby",
            "OTHER": "Other",
        }
        for name, value in expected.items():
            with self.subTest(enum="Category", name=name):
                self.assertEqual(getattr(Category, name).value, value)
                self.assertEqual(Category(value), getattr(Category, name))

    def test_frequency_enum(self):
        """Tests Frequency enum."""
        expected = {
            "DAILY": "Daily",
            "WEEKLY": "Weekly",
            "MONTHLY": "Monthly",
        }
        for name, value in expected.items():
            with self.subTest(enum="Frequency", name=name):
                self.assertEqual(getattr(Frequency, name).value, value)
                self.assertEqual(Frequency(value), getattr(Frequency, name))

    def test_invalid_enum_values(self):
        """Tests invalid enum values in all enums."""
        test_cases = {
            BackgroundColor: "Pink",
            Priority: "Urgent",
            Category: "Finance",
            Frequency: "Yearly",
        }
        for enum_cls, invalid_value in test_cases.items():
            with self.subTest(enum=enum_cls.__name__):
                with self.assertRaises(ValueError):
                    enum_cls(invalid_value)


if __name__ == "__main__":
    unittest.main()
