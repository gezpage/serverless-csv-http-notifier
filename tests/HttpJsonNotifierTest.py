import json
import unittest

from HttpNotifier import HttpNotifier


class HttpJsonNotifierTest(unittest.TestCase):
    def test_post(self):
        test_data = '{"test": "var"}'

        # Use 3rd party httpbin.org website to validate functionality
        notifier = HttpNotifier('http://httpbin.org/post')
        response = notifier.post_json_data(test_data)

        # Ensure we get a 200 OK response
        self.assertEqual(200, response['statusCode'])

        # httpbin allows access to httpd body, so we can verify it was received
        self.assertEqual(test_data, json.loads(response['response'])['data'])

        # TODO Test for failure state
        # TODO remove live http call from unit tests and create integration test
