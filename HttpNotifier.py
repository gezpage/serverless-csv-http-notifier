import json
from typing import List

import requests


class HttpNotifier:
    """ Accepts a JSON string and makes an HTTP POST to the endpoint provided in the constructor

    Utilises the Requests library

    According to the docs, connections are automatically reused, so should be relatively performant:
    http://docs.python-requests.org/en/latest/user/advanced/#keep-alive

    Note: if improved performance is desired, look at replacing Requests for PyCurl
    https://stackoverflow.com/questions/15461995/python-requests-vs-pycurl-performance
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def post_json_data(self, json_string: str) -> dict:
        response = requests.post(
            self.endpoint,
            json=json.loads(json_string)
        )
        return {
            "statusCode": response.status_code,
            "response": response.text
        }


if __name__ == "__main__":
    """ Use a list of JSON strings against a test HTTP sink """
    test_data: List[str] = ['{"test":"var"}', '{"another_test":"another_var"}']
    notifier = HttpNotifier('http://httpbin.org/post')
    for row in test_data:
        r = notifier.post_json_data(row)
        print(r)
