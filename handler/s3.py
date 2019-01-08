import boto3 as boto3


class S3:
    """ S3 specific functions

    Further S3 related functionality could be added here,
    such as moving processed files into a different bucket etc.
    """

    def __init__(self):
        self.s3 = boto3.resource("s3")

    def read_ascii_file(self, bucket, key):
        """ Get the UTF-8 content of a file in an S3 bucket """
        obj = self.s3.Object(bucket, key)

        return obj.get()["Body"].read().decode("utf-8")
