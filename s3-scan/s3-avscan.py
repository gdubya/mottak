#!/usr/bin/env python3
import os
import sys
import logging
import pyclamd
import ar_s3_helper as ar

from dotenv import load_dotenv
load_dotenv()

# To enable debugging of the boto3 library uncomment this:
# boto3.set_stream_logger('', logging.DEBUG)

def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    """
    socket = os.getenv('CLAMD_SOCK')
    csock = None
    if not socket:
        socket = '/var/run/clamav/clamd.sock'
    try:
        csock = pyclamd.ClamdUnixSocket(socket)
        csock.ping()
    except Exception as e:
        logging.error(f'Failed to ping clamav deamon over socket: {socket}')
        logging.error(f'Error: {e}')
        raise
    return csock


def scan():
    msgs = [];

    s3 = ar.get_s3_handle()
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')
    size = ar.get_object('ContentLength', s3, os.getenv(
        'BUCKET'), os.getenv('OBJECT'))
    # max_size = int(os.getenv('MAX_SCAN_SIZE') or 1024^3)
    # Don't scan files larger than ... 1GB
    #if not max_size:
    #    max_size = 1024 ^ 3
    #if (size > max_size):
    #    msgs.append("Not scanning as object is bigger than MAX_SCAN_SIZE")
    #    return None
    file_stream = ar.get_object(
        'Body', s3, os.getenv('BUCKET'), os.getenv('OBJECT'))
    if file_stream is None:
        logging.error("Could not open file.")
        raise Exception('Could not get S3 object handle')

    cd = get_clam()
    version = cd.version()
    result = cd.scan_stream(file_stream)

    with open("/tmp/av.log", "w") as log_file:
        print("AV Scan", file=log_file)
        print("Bucket:", os.getenv('BUCKET'), "@",os.getenv('REGION_NAME'),'/', os.getenv('ENDPOINT'), file=log_file)
        print("Object:", os.getenv('OBJECT'), file=log_file)
        print("Size:", size, file=log_file)
        print("Version:", version, file=log_file)
        print("Messages: ", "\n".join(msgs), file=log_file);
        print("No virus found" if not result else result, file=log_file)

    with open("/tmp/result", "w") as res_file:
        if result is None:
            print("clean", file=res_file)
            print("No viruses found")
            return None
        else:
            print("Virus found: ", result)
            print(result, file=res_file);
            return result


if __name__ == '__main__':
    ar.verify_environment(['ENDPOINT', 'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY', 'BUCKET', 'OBJECT'])

    if scan():
        sys.exit(1)
    else:
        sys.exit(0)
