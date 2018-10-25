import os

import S3
from CsvParser import CsvParser
from HttpNotifier import HttpNotifier

endpoint = os.environ.get('http_endpoint')
http_notifier = HttpNotifier(endpoint)
parser = CsvParser()


def notifier(event, context):
    """
    AWS Lambda invokable function

    Expects S3 Records data in event
    Reads CSV file contents, transforms into JSON strings, and sends an HTTP POST request with JSON body for each

    Response code will be 200 if all items successful, or 500 if any fail

    Message body will contain details on each item processed
    """
    sent = []
    status_code = 200

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        # TODO catch errors and squirrel them away in the response
        csv_data = S3.read_ascii_file(bucket, key)

        for json_string in parser.string_to_json_list(csv_data):
            item = http_notifier.post_json_data(json_string)
            item['request'] = json_string

            if item['statusCode'] != 200:
                # One or more failed (non 200) requests
                status_code = 500

            sent.append(item)

    return {
        "statusCode": status_code,
        "body": sent
    }
