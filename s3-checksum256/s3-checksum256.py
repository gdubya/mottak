#!/usr/bin/env python3
from __future__ import with_statement

import os
import sys
import logging
import hashlib
import ar_s3_helper as ar

from dotenv import load_dotenv
load_dotenv()

ENVERROR=1
FILEERROR=2

RESULT = '/tmp/result'

# To enable debugging of the boto3 library uncomment this:
# boto3.set_stream_logger('', logging.DEBUG)


def checksum():
    sha256_hash = hashlib.sha256()
    s3 = ar.get_s3_resource()
    bucket = os.getenv('BUCKET')
    filename = os.getenv('OBJECT')
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')
    obj = s3.Object(bucket, filename)
    try:
        ret = obj.get()
    except Exception as e:
        logging.error(f'S3 Error: {e}')
        
    file_stream = ret['Body']
    if file_stream is None:
        logging.error(f"Could not open file: {filename} on {bucket}")
        raise Exception('Could not get S3 object handle')

    for byte_block in iter(lambda: file_stream.read(4096), b""):
        sha256_hash.update(byte_block)
    try:
        with open(RESULT, "w") as res_file:
            checksum = sha256_hash.hexdigest()
            expected = os.getenv('CHECKSUM')
            if (checksum == expected):
                print("ok", file=res_file)
                print(f"Expected checksum '{expected}' matched {checksum}")
            else:
                print("error", file=res_file)
                print(f"Checksum mismatch. Expected'{expected}' - got {checksum}")

    except EnvironmentError as e:
        logging.error("Failed to open %s: %s" % (RESULT, e))
        exit(FILEERROR)

if not ar.verify_environment(['ENDPOINT', 'AWS_ACCESS_KEY_ID',
                              'AWS_SECRET_ACCESS_KEY', 'BUCKET', 'OBJECT']):
    exit(ENVERROR)


if __name__ == '__main__':
    if checksum():
        sys.exit(1)
    else:
        sys.exit(0)
