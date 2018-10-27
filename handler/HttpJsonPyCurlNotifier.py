import pycurl
from io import BytesIO
from typing import List


class HttpJsonPyCurlNotifier:
    """ PyCurl notifier implementation

    An alternative to using the Requests library, for performance reasons.
    (https://stackoverflow.com/questions/15461995/python-requests-vs-pycurl-performance)

    There are issues packaging this up during the Serverless deployment,
    so this is unfinished and unused.
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def post(self, json_string: str) -> dict:
        return self.post_with_pycurl(json_string)

    def post_with_pycurl(self, json_string: str) -> dict:
        # Buffer pycurl output
        buffer = BytesIO()

        # TODO Throw exceptions on error
        c = pycurl.Curl()

        # Configure JSON POST request
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, json_string)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(pycurl.URL, self.endpoint)
        c.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                     'X-Requested-By:MyClient',
                                     'Content-Type:application/json'])
        # Uncomment to allow debugging
        # c.setopt(pycurl.VERBOSE, 1)

        # Perform the HTTP request
        c.perform()

        # Prepare response data for return
        response = {
            "statusCode": c.getinfo(pycurl.RESPONSE_CODE),
            "response": buffer.getvalue().decode('utf-8')
        }

        # Close off the connection
        # TODO Allow for connection sharing between POST requests
        c.close()

        return response


if __name__ == "__main__":
    ''' Use a list of JSON strings against a test HTTP sink '''
    test_data: List[str] = ['{"test":"var"}', '{"another_test":"another_var"}']
    notifier = HttpJsonPyCurlNotifier('http://httpbin.org/post')
    for row in test_data:
        r = notifier.post(row)
        print(r)
