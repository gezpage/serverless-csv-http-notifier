import unittest
import uuid
from mock import patch

import boto3

from handler.handler import handler


class HandlerTest(unittest.TestCase):
    def setUp(self):
        self.test_csv_file = 'data/testdata.csv'
        self.s3 = boto3.client('s3')
        self.bucket = self._create_temp_s3_bucket()
        self.key = self._create_csv_test_file_in_s3()
        self.event = self._create_test_event_data()
        self.context = self._create_test_context_data()

    @patch('handler.config.get_endpoint')
    def test_handler_end_to_end(self, http_endpoint):
        """ End to end integration test for the Lambda handler

        Patches the function to get the http endpoint since I can't seem to set an environment var
        Creates a temporary S3 bucket and uploads a test CSV file
        Runs the handler and makes a live HTTP request to httpbin.org
        Asserts we get a 200 OK response
        Deletes the S3 bucket
        """
        http_endpoint.return_value = 'https://httpbin.org/post'
        response = handler(self.event, self.context)

        self.assertEqual(200, response['statusCode'])

    def tearDown(self):
        self._delete_temp_s3_bucket()

    def _create_temp_s3_bucket(self):
        bucket_name = 'json-notifier-test-bucket-' + str(uuid.uuid4())
        self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-2'
        })
        return bucket_name

    def _create_csv_test_file_in_s3(self):
        file_name = 'test-data-' + str(uuid.uuid4()) + '.csv'
        self.s3.upload_file(self.test_csv_file, self.bucket, file_name)
        return file_name

    def _create_test_event_data(self):
        return {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": self.bucket,
                        },
                        "object": {
                            "key": self.key,
                        }
                    }
                }
            ]
        }

    def _create_test_context_data(self):
        return {}

    def _delete_temp_s3_bucket(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket)
        bucket.objects.all().delete()
        bucket.delete()
