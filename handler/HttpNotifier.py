import json
from typing import List

import requests
from requests import RequestException


class HttpNotifier:
    """ Accepts a JSON string and makes an HTTP POST to the endpoint provided in the constructor

    Utilises the Requests library

    If an error is encountered, an exception is caught so that a dict can always be returned.

    According to the docs, connections are automatically reused, so should be relatively performant:
    http://docs.python-requests.org/en/latest/user/advanced/#keep-alive

    Note: if improved performance is desired, look at replacing Requests for PyCurl
    https://stackoverflow.com/questions/15461995/python-requests-vs-pycurl-performance
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def post_json_data(self, json_string: str) -> dict:
        """ POST request to the endpoint URL and response a dict with request and response data """

        request_data = {
            "requestBody": json_string
        }

        try:
            response_object = requests.post(
                self.endpoint,
                json=json.loads(json_string)
            )

            # Enable Requests exception raising so we can capture errors
            response_object.raise_for_status()

            request_data['responseBody'] = response_object.text
            request_data['statusCode'] = response_object.status_code

        except RequestException as e:
            request_data['responseBody'] = str(e.response)
            request_data['statusCode'] = 500
            request_data['error'] = str(e)

        except Exception as e:
            request_data['statusCode'] = 500
            request_data['error'] = str(e)

        return request_data


if __name__ == "__main__":
    """ Use a list of JSON strings against a test HTTP sink """
    test_data: List[str] = ['{"test":"var"}', '{"another_test":"another_var"}']
    notifier = HttpNotifier('http://httpbin.org/post')
    for row in test_data:
        r = notifier.post_json_data(row)
        print(r)
