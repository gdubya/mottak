#!/usr/bin/env python3
import os
import sys
import logging

import tarfile
import ar_s3_helper as ar

import pyclamd

from dotenv import load_dotenv
load_dotenv()

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

class S3ObjectWithTell:
    """
    Ads a tell method on the S3 object so we can give it the python tarfile lib.
    """
    def __init__(self, s3object):
        self.s3object = s3object
        self.offset = 0

    def read(self, amount=None):
        result = self.s3object.read(amount)
        self.offset += len(result)
        return result

    def close(self):
        self.s3object.close()

    def tell(self):
        return self.offset

class TarfileIterator:
    """
    Creates an iteratable object from a tarfile.
    """
    def __init__(self, tarfileobject):
        self.tarfileobject = tarfileobject

    def __iter__(self):
        return self

    def __next__(self):
        nextmember = self.tarfileobject.next()
        if nextmember:
            return nextmember
        else:
            raise StopIteration


bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')

s3 = ar.get_s3_resource()
obj = s3.Object(bucket, filename)

ret = obj.get()

file_stream = S3ObjectWithTell(ret['Body'])

if file_stream is None:
    logging.error("Could not open file.")
    raise Exception('Could not get S3 object handle')

tfi = None
try:
    tf = tarfile.open(fileobj=file_stream, mode='r|')
    mytfi = TarfileIterator(tf)
    tfi = iter(mytfi)
except:
    logging.error(f'Failed to open stream to object: {bucket} / {filename}')
    logging.error(f'Error: {e}')
    raise

cd = None
try:
    cd = get_clam()
    cver = cd.version()
    print(f'Intializing scan on {bucket}/{filename} using {cver}')
except:
    logging.error("Failed to connect to ClamAV")
    logging.error(f'Error: {e}')
virus = 0

for member in tfi:
    handle = tf.extractfile(member)
    if handle == None:
        # Handle is none - likely a directory.
        continue
    # print(handle.read())
    try:
        result = cd.scan_stream(handle)
        if (result is None):
            print(f'OK - {member.name}')
        else:
            print(f'Virus found! {result["stream"][1]} in {member.name}')
            virus += 1
    except:
        logging.error(f"Failed to scan {member.name}")
        logging.error(f'Error: {e}')


print("========")
print(f"{virus} viruses found")


