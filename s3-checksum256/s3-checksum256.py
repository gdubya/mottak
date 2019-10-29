#!/usr/bin/env python3
import os
import sys
import logging
import hashlib
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from dotenv import load_dotenv
load_dotenv()

# To enable debugging of the boto3 library uncomment this:
# boto3.set_stream_logger('', logging.DEBUG)


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


def verify_environment():
    """Verify that the required environment variables are set.
    exits if is unhappy.
    """
    reqs = ['ENDPOINT', 'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY', 'BUCKET', 'OBJECT']
    for req in reqs:
        if not os.getenv(req):
            logging.error('Environment variable ' + req + ' is not set')
            sys.exit(2)



def get_s3_handle():
    """Create an S3 client object.

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

def checksum():
    sha256_hash = hashlib.sha256()

    verify_environment()
    s3 = get_s3_handle()
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')
    file_stream = get_object(
        'Body', s3, os.getenv('BUCKET'), os.getenv('OBJECT'))
    if file_stream is None:
        logging.error("Could not open file.")
        raise Exception('Could not get S3 object handle')

    for byte_block in iter(lambda: file_stream.read(4096),b""):
        sha256_hash.update(byte_block)
    print(sha256_hash.hexdigest())

if __name__ == '__main__':
    if checksum():
        sys.exit(1)
    else:
        sys.exit(0)
