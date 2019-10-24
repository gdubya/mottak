#!env python
import os
import logging
import pyclamd
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from dotenv import load_dotenv
load_dotenv()


def get_object(objectstore, bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """
    try:
        response = objectstore.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return None
    return response['Body']


def get_s3_handle():
    client_handle = None
    print("S3 point for", os.getenv('AWS_ACCESS_KEY_ID'),":", os.getenv('AWS_SECRET_ACCESS_KEY'))
    
    try:
        client_handle = boto3.client('s3', 
                          endpoint_url=os.getenv('ENDPOINT'),
                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          config=Config(signature_version='s3v4'),
                          region_name=os.getenv('REGION_NAME'))
    except:
        print("Could not create client handle")
        raise
    return client_handle



def main():
    s3 = get_s3_handle()
    file_stream = get_object(s3, os.getenv('BUCKET'), "test.txt")
    cd = pyclamd.ClamdUnixSocket(os.getenv('CLAMD_SOCK'))
    try:
        cd.ping()
    except Exception as e:
        print("Failed to ping clamav deamon over socket:",os.getenv('CLAMD_SOCK') )
        raise
    print(cd.version())
    print("Opening stream to ClamAV")
    #dump_stream(file_stream)
    print(cd.scan_stream(file_stream))


if __name__ == '__main__':
    main()
