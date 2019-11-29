import sys
import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging

def verify_environment(reqs):
    """Verify that the required environment variables are set.
    :return: True - everything is OK, False otherwise
    """

    for req in reqs:
        if not os.getenv(req):
            logging.error('Environment variable ' + req + ' is not set')
            return False
    return True



def eprint(*args, **kwargs):
    """ Print to stderr """
    print(*args, file=sys.stderr, **kwargs)


def get_s3_handle():
    """Create an S3 client object based on ENDPOINT, REGION_NAME using AWS_ACCESS_KEY_ID
    and AWS_SECRET_ACCESS_KEY

    :return: boto3.client object. If error, return None.
    """

    client_handle = None

    try:
        client_handle = boto3.client(service_name='s3',
                                     endpoint_url=os.getenv('ENDPOINT'),
                                     aws_access_key_id=os.getenv(
                                         'AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv(
                                         'AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('REGION_NAME'))
    except Exception as e:
        logging.error(e, stack_info=True)
        return None
    return client_handle


def get_object(what, objectstore, bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param what: string of what to get: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    :param objectstore: boto3.client object
    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """
    try:
        response = objectstore.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return None
    return response[what]

