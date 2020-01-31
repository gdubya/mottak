#!/usr/bin/env python3
import os
import sys
import logging

import tarfile
import ar_s3_helper as ar

import subprocess as sp     # execute siegfried
# For compatibility with Python 3.6 (capture_output)
from subprocess import PIPE
import csv   # parsing siegfried output
import io    # string to IO

import re

import json

from dotenv import load_dotenv
load_dotenv()

global pronom_types       # dict resulting from parsing the pronom definitions
global csv_log            # dict for logging convertions

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
    action = None
    if id in pronom_types:
        action = pronom_types[id]['convert']

    return action


# Converters
"""
convert_libreoffice(path, file)
Calls out to libreoffice in headless to convert a file to PDF.
"""


def convert_libreoffice(path, file):
    res = None
    try:
        cmdline = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.getenv('TMPWORKSPACE'), f'{path}/{file}']
        print(f"Converting {file} in {path}:", cmdline)
        res = sp.run(cmdline,
                     shell=False, stderr=PIPE, timeout=180)
        if (res.stderr):
            print("WARNING: libreoffice talked on STDERR:", res.stderr)
    except Exception as e:
        logging.error("Error while running headless libreoffice...")
        logging.error(f'Error: {e}')
        raise(e)
    # print(f"Ret, Output:", res.returncode, res.stdout)
    return '.pdf'


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

# Todo: wash away any trailing / from tmpdir
tmpdir = os.getenv('TMPWORKSPACE')
uuid = os.getenv('UUID')

for member in tfi:
    # try:
    # We only care about files.
    if member.isfile():
        # Skip stuff that isn't in $uuid/content (metadata)
        if not re.search(f'^{uuid}/content', member.name):
            continue
        handle = tf.extract(member, tmpdir)
        s_output = siegfried(tmpdir, member.name)
        # keys in the dict we get back:
        # filename,filesize,modified,errors,namespace,id,format,version,mime,basis,warning
        new_extension = ''
        action = get_action(s_output['id'], s_output['format'])
        if (action == 'skip'):
            continue
        elif (action == 'libreoffice'):
            new_extension = convert_libreoffice(tmpdir, member.name)
        else:
            print(f"File '{member.name} has unknown pronom type: {s_output['id']}")
            continue

        # Build new path
        orgwithoutext = (os.path.splitext(member.name))[0]
        basenamewithoutext = os.path.basename(orgwithoutext)
        # New path for object store
        objectname = orgwithoutext + new_extension
        # Where is the converted file:
        converted_file = tmpdir + '/'+ basenamewithoutext + new_extension
        print(f"Uploading {converted_file} ===> {objectname}")
        workspace_bucket.upload_file(converted_file, objectname)


   # except Exception as e:
   #    logging.error(f"Failed to extract and process {member.name}")
   #    logging.error(f'Error: {e}')


print("========")
