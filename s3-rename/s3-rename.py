#!/usr/bin/env python3
import os
import sys
import logging
import ar_s3_helper as ar

from dotenv import load_dotenv
load_dotenv()

ENVERROR = 1
RENAMEERROR = 2

def rename():
    filename = os.getenv('OBJECT')
    newname = os.getenv('NEWNAME')
    bucket = os.getenv('BUCKET')
    s3 = ar.get_s3_resource()
    if s3 is None:
        logging.error("S3 client handle not defined")
        raise Exception('S3 client handle not defined')
    print(f'Copying {filename} to {newname} in {bucket}')
    if ar.bucket_copy_object(objectstore=s3, bucket_name=bucket,
                             object_name=filename, target=newname):
        logging.info(f"Renamed {filename} succesfully from {bucket} to {newname}")
        return(True)
    else:
        logging.error(f"Failed to rename {filename} from {bucket} to {newname}")
        return(False)

if ar.verify_environment(['ENDPOINT', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                          'REGION_NAME', 'BUCKET', 'OBJECT', 'NEWNAME']):
    logging.info("Environment verified OK")
else:
    logging.error("Enviroment not set properly")
    exit(ENVERROR)

if __name__ == '__main__':
    if rename():
        sys.exit(0)
    else:
        sys.exit(RENAMEERROR)
