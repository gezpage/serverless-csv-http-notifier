import logging
import os


def get_endpoint():
    return str(os.environ.get("http_endpoint"))


def get_logging_level():
    return logging.INFO
