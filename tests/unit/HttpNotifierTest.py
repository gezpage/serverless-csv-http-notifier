import unittest

from requests_mock import Mocker as mock_requests

from handler.HttpNotifier import HttpNotifier


@mock_requests()
class HttpNotifierTest(unittest.TestCase):
    def setUp(self):
        self.sut = HttpNotifier("http://test.com")

    def test_post_json_data_success(self, m):
        test_data = '{"Var name": "Value"}'
        m.post("http://test.com", text="OK")

        data = self.sut.post_json_data(test_data)

        # Successful post should come back with a dict with 3 items
        self.assertEqual(test_data, data["requestBody"])
        self.assertEqual("OK", data["responseBody"])
        self.assertEqual(200, data["statusCode"])

    def test_post_json_data_success_exception_handling(self, m):
        test_data = '{"Var name": "Value"}'
        m.post("http://test.com", exc=Exception)

        data = self.sut.post_json_data(test_data)

        # Failed post should catch the exception and still return the dict
        self.assertEqual(test_data, data["requestBody"])
        self.assertEqual(500, data["statusCode"])
