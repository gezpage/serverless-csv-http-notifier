import unittest

import requests_mock
from mock import mock

from handler.Notifier import Notifier


class NotifierTest(unittest.TestCase):
    """ Test of the lambda handler function

    Intended to test the entire function without actually hitting the live S3 service or making a real HTTP request

    TODO - Test more failure states
    """

    def setUp(self):
        self.notifier = Notifier('http://test.com')

    def valid_s3_file_contents(self, key):
        """ The mock data to be returned by s3.read_ascii_file """
        return '''"First name", "Last name", "Email"
        "Dave", "Banks", "davebanks@email.com"
        "Grant", "Davis", "grantdavis@email.com"'''

    def invalid_s3_file_contents(self, key):
        """ The mock data to be returned by s3.read_ascii_file """
        return ''

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

        Using requests_mock to mock an HTTP request
        Mocking the s3.read_ascii_file function to return test CSV data

        Currently only checking for a 200 status code in the handler return data
        """
        m.post('http://test.com', text='OK')

        self.notifier.process(self.records_data())

        processed = self.notifier.processed

        # Ensure we have an overall 200 status with 1 file (batch) processed
        self.assertEqual(200, self.notifier.status_code)
        self.assertEqual(1, len(processed))

        batch = processed[0]

        # Should have 2 items in the batch with 200 status
        self.assertEqual(2, len(batch['items']))
        self.assertEqual(200, batch['items'][0]['statusCode'])
        self.assertEqual(200, batch['items'][1]['statusCode'])

        requests = m.request_history

        # Ensure 2 (mocked) requests were made with expected JSON
        self.assertEqual(2, len(requests))
        self.assertEqual('{"First name": "Dave", "Last name": "Banks", "Email": "davebanks@email.com"}', requests[0].text)
        self.assertEqual('{"First name": "Grant", "Last name": "Davis", "Email": "grantdavis@email.com"}', requests[1].text)

    @requests_mock.Mocker()
    @mock.patch('handler.S3.S3.read_ascii_file', side_effect=invalid_s3_file_contents)
    def test_processing_invalid_csv_data(self, m, urandom_function):
        m.post('http://test.com', text='OK')

        self.notifier.process(self.records_data())

        processed = self.notifier.processed

        # Ensure we have an overall 500 status with 0 file (batch) processed
        self.assertEqual(500, self.notifier.status_code)
        self.assertEqual(0, len(processed))
