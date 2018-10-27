from handler.Notifier import Notifier


def handler(event, context):
    """
    AWS Lambda invokable function

    Expects S3 Records data in event

    Response code will be 200 if all items successful, or 500 if any fail

    Message body will contain details on each file processed
    """

    notifier = Notifier()
    notifier.process(event['Records'])

    return {
        "statusCode": notifier.status_code,
        "body": notifier.processed
    }
