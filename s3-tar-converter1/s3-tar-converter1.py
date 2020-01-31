#!/usr/bin/env python3
import os
import sys
import logging

import tarfile
import ar_s3_helper as ar

import subprocess as sp     # execute siegfried
from subprocess import PIPE # For compatibility with Python 3.6 (capture_output)
import csv   # parsing siegfried output
import io    # string to IO

import json

from dotenv import load_dotenv
load_dotenv()

global pronom_types


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

def process_sf_csv(output):
    reader_list = csv.DictReader(io.StringIO(output))
    return reader_list

def siegfried(path, file):
    sf_run = ''

    sf_run = sp.run(['sf', '-csv', f'{path}/{file}'], stdout=PIPE)
    res = process_sf_csv(sf_run.stdout.decode('utf-8´'))

    return(next(res))

def get_action(id, format):
    global pronom_types
    # Looking up action for id
    action = ''
    if not id in pronom_types:
        print("Unknown pronom type:", id)
        print("Format:", format)
    else:
        action = pronom_types[id]['convert']

    return action

##########################
#  Execute from here:
##########################

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')

s3 = ar.get_s3_resource()
workspace_bucket = s3.Bucket(os.getenv('WORKSPACE'))
obj = s3.Object(bucket, filename)

ret = obj.get()

file_stream = S3ObjectWithTell(ret['Body'])
pronom_types = json.loads(open(f'pronomtypes.json').read())


if file_stream is None:
    logging.error("Could not open file.")
    raise Exception('Could not get S3 object handle')

tfi = None
try:
    tf = tarfile.open(fileobj=file_stream, mode='r|')
    mytfi = TarfileIterator(tf)
    tfi = iter(mytfi)
except Exception as e:
    logging.error(f'Failed to open stream to object: {bucket} / {filename}')
    logging.error(f'Error: {e}')
    raise


tmpdir = os.getenv('TMPDIR')
for member in tfi:
    #try:
        # We only care about files.
        if member.isfile():
            handle = tf.extract(member, tmpdir)
            s_output = siegfried(tmpdir, member.name)
            # Key
            # filename,filesize,modified,errors,namespace,id,format,version,mime,basis,warning
            print("File:", member.name)
            #print(s_output)
            action = get_action(s_output['id'], s_output['format'])
            print(" Pronom:", s_output['id'], "Action:", action)
            print("Uploading")
            workspace_bucket.upload_file(f'{tmpdir}/{member.name}', member.name)
            # print(" Format", s_output['format'])

   # except Exception as e:
   #    logging.error(f"Failed to extract and process {member.name}")
   #    logging.error(f'Error: {e}')


print("========")


