#!/usr/bin/env python3
import os
import sys
import logging

import tarfile
from py_objectstore import ArkivverketObjectStorage, MakeIterIntoFile, TarfileIterator

import pyclamd

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("Failed to load dotenv file. Assuming production")

def get_clam():
    """Establish connection with Clamd
    :return: pyclamd socket object
    """
    socket = os.getenv('CLAMD_SOCK', default='/var/run/clamav/clamd.ctl')
    csock = None
    try:
        csock = pyclamd.ClamdUnixSocket(socket)
        csock.ping()
    except Exception as e:
        logging.error(f'Failed to ping clamav deamon over socket: {socket}')
        logging.error(f'Error: {e}')
        raise
    return csock

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')
avlogfile = os.getenv('AVLOG', default='/tmp/avlog')
storage = ArkivverketObjectStorage()

obj = storage.download_stream(bucket, filename)

file_stream = MakeIterIntoFile(obj)

if file_stream is None:
    logging.error("Could not open file.")
    raise Exception('Could not get object handle')

tfi = None
try:
    tf = tarfile.open(fileobj=file_stream, mode='r|')
    mytfi = TarfileIterator(tf)
    tfi = iter(mytfi)
except Exception as e:
    logging.error(f'Failed to open stream to object: {bucket} / {filename}')
    logging.error(f'Error: {e}')
    raise

cd = None
try:
    cd = get_clam()
    cver = cd.version()
    print(f'Intializing scan on {bucket}/{filename} using {cver}')
except Exception as e:
    logging.error("Failed to connect to ClamAV")
    logging.error(f'Error: {e}')
virus = 0

with open(avlogfile,mode='w') as avlog:
    for member in tfi:
        handle = tf.extractfile(member)
        if handle == None:
            # Handle is none - likely a directory.
            continue
        # print(handle.read())
        try:
            result = cd.scan_stream(handle)
            if (result is None):
                print(f'OK - {member.name}', file=avlog)
            else:
                print(f'Virus found! {result["stream"][1]} in {member.name}', file=avlog)
                virus += 1
        except Exception as e:
            logging.error(f"Failed to scan {member.name}")
            logging.error(f'Error: {e}')
            raise(e)
    print("========", file=avlog)
    print(f"{virus} viruses found", file=avlog)
    print(f"Archive scanned. Log created as {avlogfile}")





