from CsvParser import CsvParser
from HttpJsonNotifier import HttpJsonNotifier

# endpoint: str = 'http://localhost:8010'
endpoint: str = 'http://httpbin.org/post'


def notifier(event, context):
    """
    AWS Lambda invokable function

    Accepts CSV string data as the function event,
    transforms into JSON strings, and sends an HTTP POST request with the JSON body

    """
    http_notifier = HttpJsonNotifier(endpoint)
    parser = CsvParser()
    sent = []

    # Parse the CSV data and iterate through the list of JSON strings returned
    for json_string in parser.string_to_json_list(event):
        # Use the HTTP notifier to make a POST request with the JSON as the body
        response = http_notifier.post(json_string)
        # If the response from the notifier endpoint is JSON, uncomment this line to parse it into the handler response
        # response['response'] = json.loads(response['response'])
        sent.append(response)

    response = {
        "statusCode": 200,
        "body": sent
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
