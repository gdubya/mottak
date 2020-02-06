#!/usr/bin/env python3
import os
import sys
import logging

import tarfile

from av_objectstore import ArkivverketObjectStorage
from av_objectstore import MakeIterIntoFile
from av_objectstore import TarfileIterator

import subprocess as sp     # execute siegfried
# For compatibility with Python 3.6 (capture_output)
from subprocess import PIPE
import csv   # parsing siegfried output
import io    # string to IO

import tempfile

import re

import json

from dotenv import load_dotenv
load_dotenv()


global pronom_types       # dict resulting from parsing the pronom definitions
global csv_log            # dict for logging convertions


def process_sf_csv(output):
    reader_list = csv.DictReader(io.StringIO(output))
    return reader_list


def siegfried(file):
    sf_run = ''

    sf_run = sp.run(['sf', '-csv', file], stdout=PIPE)
    res = process_sf_csv(sf_run.stdout.decode('utf-8´'))

    return(next(res))


def get_action(id, format):
    global pronom_types
    # Looking up action for id
    action = None
    if id in pronom_types:
        action = pronom_types[id]['convert']

    return action


def make_csv_row(row):
    line = ','.join(map(lambda x: f'"{x}"',  row))
    return line.encode('utf-8')


def upload_csv(storage, objectname, loglist, bucket):
    csvlines = iter(map(lambda x: make_csv_row(x), loglist))
    try:
        storage.upload_stream(
            container=bucket, name=objectname, iterator=csvlines)
    except Exception as e:
        logging.error("Error while uploading CSV")
        raise "Error while uploading CSV"
        


# Converters
"""
convert_libreoffice(path, file)
Calls out to libreoffice in headless to convert a file to PDF.
"""


def convert_libreoffice(path, file):
    res = None
    try:
        cmdline = ['libreoffice', '--headless', '--convert-to', 'pdf',
                   '--outdir', os.getenv('TMPWORKSPACE'), f'{path}/{file}']
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
workspace = os.getenv('WORKSPACE')

storage = ArkivverketObjectStorage()

tar_obj = storage.download_stream(bucket, filename)

# Initialize the csv_log (LoL) with headers:
csv_log = [['old_name', 'old_pronom', 'new_name', 'new_pronom']]

tar_file_stream = MakeIterIntoFile(tar_obj)
# Load the pronomnoms.
pronom_types = json.loads(open(f'pronomtypes.json').read())

if tar_file_stream is None:
    logging.error("Could not open file.")
    raise Exception('Could not get object handle')

tfi = None
try:
    tf = tarfile.open(fileobj=tar_file_stream, mode='r|')
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
        siegfried_org_file = siegfried(tmpdir + '/' + member.name)
        # keys in the dict we get back:
        # filename,filesize,modified,errors,namespace,id,format,version,mime,basis,warning
        new_extension = ''
        action = get_action(
            siegfried_org_file['id'], siegfried_org_file['format'])
        if (action == 'skip'):
            continue
        elif (action == 'libreoffice'):
            new_extension = convert_libreoffice(tmpdir, member.name)

        else:
            print(
                f"File '{member.name} has unknown pronom type: {siegfried_org_file['id']}")
            continue

        # at this point we know that a conversion has taken place. The converted file is in /tmpdir/
        # Build new path
        orgwithoutext = (os.path.splitext(member.name))[0]
        basenamewithoutext = os.path.basename(orgwithoutext)
        # New path for object store
        objectname = orgwithoutext + new_extension
        # Where is the converted file:
        converted_file = tmpdir + '/' + basenamewithoutext + new_extension
        print(f"Uploading {converted_file} ===> {objectname}")
        storage.upload_file(workspace, objectname, converted_file, )
        # Now we log it.

        # We need the new pronom code:
        siegfried_new_file = siegfried(converted_file)

        csv_log.append([
            member.name, siegfried_org_file['id'],
            objectname, siegfried_new_file['id']])

   # except Exception as e:
   #    logging.error(f"Failed to extract and process {member.name}")
   #    logging.error(f'Error: {e}')

print("========")
print("Conversion done. Uploading CSV.")

upload_csv(storage=storage, objectname=f'{uuid}.csv', loglist=csv_log,
           bucket=workspace)
