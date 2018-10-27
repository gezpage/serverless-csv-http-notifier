import unittest

import requests_mock
from mock import mock

from handler import config
from handler.Notifier import Notifier


class NotifierTest(unittest.TestCase):
    """ Test of the lambda handler function

    Intended to test the entire function without actually hitting the live S3 service or making a real HTTP request

    TODO - Test more failure states
    """

    def setUp(self):
        self.notifier = Notifier()

    def valid_s3_file_contents(self, key):
        """ The mock data to be returned by s3.read_ascii_file """
        return '''"First name", "Last name", "Email"
        "Dave", "Banks", "davebanks@email.com"
        "Grant", "Davis", "grantdavis@email.com"
        '''

    def invalid_s3_file_contents(self, key):
        """ The mock data to be returned by s3.read_ascii_file """
        return '''not "csv" data!@#$%^&*()'''

    def records_data(self):
        """ Records normally provided in the event from s3 trigger source
        Values here are not important as the s3 call is mocked
        """
        return [
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

    @requests_mock.Mocker()
    @mock.patch('handler.S3.S3.read_ascii_file', side_effect=valid_s3_file_contents)
    def test_processing_valid_csv_data_and_notifying_endpoint(self, m, urandom_function):
        """ Notifier function test

        Using requests_mock to prevent a live HTTP request
        Also mocking the s3.read_ascii_file function to return test CSV data

        Currently only checking for a 200 status code in the handler return data
        """
        m.post(config.get_endpoint, text='OK')

        self.notifier.process(self.records_data())

        # TODO inspect request body to verify JSON
        self.assertEqual(200, self.notifier.status_code)

    @mock.patch('handler.S3.S3.read_ascii_file', side_effect=invalid_s3_file_contents)
    def test_processing_invalid_csv_data(self, urandom_function):
        # self.assertRaises(Exception, self.notifier.process(self.records_data()))
        # TODO fix this test - should throw exception on malformed CSV
        self.notifier.process(self.records_data())

