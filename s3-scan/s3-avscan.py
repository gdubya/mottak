#!/usr/bin/env python3
import os
import sys
import logging
import pyclamd
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from dotenv import load_dotenv
load_dotenv()


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
    """Verify that the required environment variables are set
    exits if is unhappy.
    """
    reqs = ['ENDPOINT', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'BUCKET', 'OBJECT']
    for req in reqs:
        if not os.getenv(req):
            logging.error('Environment variable '+ req + ' is not set')
            sys.exit(2)
        

def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    """
    socket = os.getenv('CLAMD_SOCK')
    csock = None
    if not socket:
        socket =  '/tmp/clamd.socket'
    try:
        csock = pyclamd.ClamdUnixSocket(socket)
        csock.ping()
    except Exception as e:
        print("Failed to ping clamav deamon over socket:",os.getenv('CLAMD_SOCK') )
        raise
    return csock


def get_s3_handle():
    """Retrieve an object from an Amazon S3 bucket

    :return: boto3.client object. If error, return None.
    """

    client_handle = None
    
    try:
        client_handle = boto3.client('s3', 
                          endpoint_url=os.getenv('ENDPOINT'),
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          config=Config(signature_version='s3v4'),
                          region_name=os.getenv('REGION_NAME'))
    except Exception as e:
        logging.error(e)
        return None
    return client_handle



def scan():
    verify_environment()
    s3 = get_s3_handle()
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')
    size = get_object('ContentLength', s3, os.getenv('BUCKET'), os.getenv('OBJECT'))
    max_size = int(os.getenv('MAX_SCAN_SIZE'));
    if not max_size: max_size = 1024^3;
    if (size > max_size):
        print("Not scanning as object is bigger than MAX_SCAN_SIZE")
        return None
    print('Scanning', os.getenv('OBJECT'), 'from', os.getenv('BUCKET'), ' Size: ', size)
    file_stream = get_object('Body', s3, os.getenv('BUCKET'), os.getenv('OBJECT'))
    if file_stream is None: 
        logging.error("Could not open file.")
        raise Exception('Could not get S3 object handle')

    cd = get_clam()
    print(cd.version())

    result = cd.scan_stream(file_stream)
    if result is None:
        print("No viruses found")
        return None
    else:
        print("Virus found: ", result)
        return result

if __name__ == '__main__':
    if scan():
        sys.exit(1)
    else:
        sys.exit(0)
