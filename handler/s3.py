import boto3 as boto3

""" 
S3 specific functions

Further S3 related functionality could be added here,
such as moving processed files into a different bucket etc.
"""


def read_ascii_file(bucket, key):
    """ Get the UTF-8 content of a file in an S3 bucket """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)

    return obj.get()['Body'].read().decode('utf-8')
