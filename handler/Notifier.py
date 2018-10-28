import logging
from datetime import datetime

from handler import config
from handler.CsvParser import CsvParser
from handler.HttpNotifier import HttpNotifier
from handler.S3 import S3


class Notifier:
    """
    Reads CSV file contents from S3, transforms into JSON strings, and send an HTTP POST request with JSON body for each

    Response code will be 200 if all items successful, or 500 if any fail

    Message body will contain details on each file processed
    """

    def __init__(self, http_endpoint):
        self.logger = logging.getLogger()
        self.logger.setLevel(config.get_logging_level())
        self.logger.info('Notifier endpoint: ' + http_endpoint)
        self.s3 = S3()
        self.parser = CsvParser()
        self.http_notifier = HttpNotifier(http_endpoint)

        self.status_code = 200
        self.processed = []

    def process(self, records):
        """ Accepts records data from S3 triggered event payload

        Returns a dict with batches processed containing each http request sent
        """

        for s3_file in records:
            bucket = s3_file['s3']['bucket']['name']
            key = s3_file['s3']['object']['key']

            self._process_file(bucket, key)

    def _process_file(self, bucket, key):
        batch = {
            'time': str(datetime.utcnow()),
            'bucket': bucket,
            'file': key,
            'items': []
        }

        self.logger.info('Starting batch: ' + str(batch))

        try:
            self.logger.info('Get file contents from S3')
            csv_data = self.s3.read_ascii_file(bucket, key)

            if not csv_data:
                self._process_failed()
                return

            self.logger.info('Parse CSV data: ' + csv_data)
            json_data = self.parser.string_to_json_list(csv_data)

            batch['items'] = self._notify_http_endpoint(json_data)

        except Exception as e:
            batch['error'] = str(e)
            self.logger.error('Exception caught: ' + str(e))
            self._process_failed()
        self.processed.append(batch)

    def _process_failed(self):
        self.status_code = 500

    def _notify_http_endpoint(self, json_data):
        responses = []

        for json_string in json_data:
            self.logger.info('Notifying HTTP endpoint')
            response = self.http_notifier.post_json_data(json_string)

            if response['statusCode'] != 200:
                self._process_failed()

            self.logger.info(response)
            responses.append(response)

        return responses
