import logging
from datetime import datetime

from handler import s3, config
from handler.CsvParser import CsvParser
from handler.HttpNotifier import HttpNotifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Notifier endpoint: ' + config.get_endpoint())

http_notifier = HttpNotifier(config.get_endpoint())
parser = CsvParser()


def notifier(event, context):
    """
    AWS Lambda invokable function

    Expects S3 Records data in event
    Reads CSV file contents, transforms into JSON strings, and sends an HTTP POST request with JSON body for each

    Can accept multiple files in one hit

    Response code will be 200 if all items successful, or 500 if any fail

    Message body will contain details on each file processed
    """
    processed = []
    status_code = 200

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        batch = {
            'time': str(datetime.utcnow()),
            'bucket': bucket,
            'file': key,
            'items': []
        }

        logger.info('Starting batch: ' + str(batch))

        try:
            logger.info('Get file contents from S3')
            csv_data = s3.read_ascii_file(bucket, key)

            logger.info('Parse CSV data: ' + csv_data)
            for json_string in parser.string_to_json_list(csv_data):
                logger.info('Notifying HTTP endpoint')

                response = http_notifier.post_json_data(json_string)

                batch['items'].append(response)
                logger.info(response)

        except Exception as e:
            batch['error'] = str(e)
            logger.error('Error caught: ' + str(e), {
                'bucket': bucket
            })
            status_code = 500

        processed.append(batch)

    return {
        "statusCode": status_code,
        "body": processed
    }
