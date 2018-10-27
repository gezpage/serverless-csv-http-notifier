import unittest

import requests_mock
from mock import mock

from handler import handler, config


class HttpNotifierTest(unittest.TestCase):
    """ Test of the lambda handler function

    Intended to test the entire function without actually hitting the live S3 service or making a real HTTP request
    """

    def setUp(self):
        self.handler = handler.notifier

    def s3_file_contents(self, key):
        """ The mock data to be returned by s3.read_ascii_file """
        return '''"First name", "Last name", "Email"
        "Dave", "Banks", "davebanks@email.com"
        "Grant", "Davis", "grantdavis@email.com"
        '''

    def event_data(self):
        """ The minimum event data needed for the function to work
        Values are not important as the s3 call is mocked
        """
        return {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "some-bucket",
                        },
                        "object": {
                            "key": "testdata.csv",
                        }
                    }
                }
            ]
        }

    @requests_mock.Mocker()
    @mock.patch('handler.s3.read_ascii_file', side_effect=s3_file_contents)
    def test_handler(self, m, urandom_function):
        """ Handler function test

        Using requests_mock to prevent a live HTTP request
        Also mocking the s3.read_ascii_file function to return test CSV data

        Currently only checking for a 200 status code in the handler return data
        """
        m.post(config.get_endpoint, text='OK')

        event = self.event_data()
        context = {}

        response = self.handler(event, context)

        self.assertEqual(200, response['statusCode'])
