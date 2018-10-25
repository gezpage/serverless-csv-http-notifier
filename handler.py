import json
import os


from CsvParser import CsvParser
from HttpNotifier import HttpNotifier


def notifier(event, context):
    """
    AWS Lambda invokable function

    Accepts CSV string data in the function event,
    transforms into JSON strings, and sends an HTTP POST request with JSON body

    """

    # Get the HTTP endpoint URL from the environment var
    endpoint = os.environ.get('http_endpoint')

    # Create an instance of our HTTP JSON notifier
    http_notifier = HttpNotifier(endpoint)

    # Instance of our CSV parser that will transform it to JSON
    parser = CsvParser()

    # Retrieve the CSV string from the event
    csv_data = event['csv']

    sent = []

    # Parse the CSV data and iterate through the list of JSON strings returned
    for json_string in parser.string_to_json_list(csv_data):
        # Make the POST request with the JSON
        # TODO use a try / catch and log errors
        response = http_notifier.post_json_data(json_string)

        # If the response from the notifier endpoint is JSON, uncomment this line to parse it into the handler response
        response['response'] = json.loads(response['response'])
        sent.append(response)

    response = {
        "statusCode": 200,
        "body": sent
    }

    return response
