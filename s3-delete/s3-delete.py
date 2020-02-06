#!/usr/bin/env python3
import os
import sys
import logging
from av_objectstore import ArkivverketObjectStorage

from dotenv import load_dotenv
load_dotenv()

ENVERROR = 1
DELETEERROR = 2

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')

storage = ArkivverketObjectStorage()
if storage.delete(bucket, filename):
    logging.info(f"Object deleted {filename} succesfully from {bucket}")
    sys.exit(0)
else:
    logging.error(f"Failed to delete {filename} from {bucket}")
    sys.exit(DELETEERROR)
