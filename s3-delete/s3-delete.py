#!/usr/bin/env python3
import os
import sys
import logging
import ar_s3_helper as ar

from dotenv import load_dotenv
load_dotenv()

ENVERROR = 1
DELETEERROR = 2

def delete():
    filename = os.getenv('OBJECT')
    bucket = os.getenv('BUCKET')

    s3 = ar.get_s3_resource()
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')

    obj = s3.Object(bucket, filename)

    if obj.delete():
        logging.info(f"Object deleted {filename} succesfully from {bucket}")
        return(True)
    else:
        logging.error(f"Failed to delete {filename} from {bucket}")
        return(False)


if ar.verify_environment(['ENDPOINT', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'REGION_NAME', 'BUCKET', 'OBJECT']):
    logging.info("Environment verified OK")
else:
    logging.error("Enviroment not set properly")
    exit(ENVERROR)

if __name__ == '__main__':
    if delete():
        sys.exit(0)
    else:
        sys.exit(DELETEERROR)
