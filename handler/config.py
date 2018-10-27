import os


def get_endpoint():
    return str(os.environ.get('http_endpoint'))
