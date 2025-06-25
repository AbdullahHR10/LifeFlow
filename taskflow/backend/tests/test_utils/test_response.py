"""Module that contains the response unittests."""

import unittest
from backend.tests.base_test import BaseTestCase
from backend.utils.response import json_response


class TestResponseUtils(BaseTestCase):
    def test_json_response(self):
        """Tests the json_response function output structure."""
        with self.app.test_request_context():
            response = json_response(
                status="success",
                data={"id": 1},
                message="Done"
            )
            json_data = response.get_json()
            self.assertEqual(json_data["status"], "success")
            self.assertEqual(json_data["data"], {"id": 1})
            self.assertEqual(json_data["message"], "Done")

    def test_json_response_defaults(self):
        """Tests the json_response function with only status passed."""
        with self.app.test_request_context():
            response = json_response(status="error")
            json_data = response.get_json()

            self.assertEqual(json_data["status"], "error")
            self.assertIsNone(json_data["data"])
            self.assertEqual(json_data["message"], "")


if __name__ == "__main__":
    unittest.main()
