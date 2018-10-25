import boto3 as boto3


def read_ascii_file(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8')
