#!/usr/bin/env python3
import os
import sys
import logging

import tarfile

import io
import csv # parse the CVS from the objectstore.

from av_objectstore import ArkivverketObjectStorage
from av_objectstore import MakeIterIntoFile

import tempfile
from dotenv import load_dotenv
load_dotenv()

global csv_list

def get_files(storage, bucket, uuid):
    """
    get_csv - fetch the list of files from the CSV ($uuid.csv)
    and return it.
    """
    tmpfile = tempfile.NamedTemporaryFile(mode='w')
    storage.download_file(container=bucket, name=f'{uuid}.csv', file=tmpfile.name)
    tmphandle = open(tmpfile.name, mode='r')
    csvreader = csv.reader(tmphandle)
    csvreader.__next__()
    mylist = []
    for row in csvreader:
        mylist.append(row[2])
    return mylist

"""
 We create our own file-like object to write binary data to 
 stdout
"""
class stdoutIO(io.BytesIO):
    def write(self, data):
        # print(f'Writing {len(data)} to stdout', file=sys.stderr)
        sys.stdout.buffer.write(data)
        return

    def close(self):
        # print(f'Closing file....', file=sys.stderr)
        pass
    

        

filename         = os.getenv('OBJECT')
uuid             = os.getenv('UUID')
workspace_bucket = os.getenv('WORKSPACE')

storage = ArkivverketObjectStorage()


csv_list = get_files(storage,  workspace_bucket, uuid)


# fp = os.fdopen(sys.stdout.fileno(), 'wb')
fp = stdoutIO()

tf = tarfile.open(fileobj=fp, mode='w|')
for file in csv_list:
    size = int(storage.get_size(workspace_bucket, file))
    #print(file, size)
    tarinfo = tarfile.TarInfo(name=file)
    stream = MakeIterIntoFile(storage.download_stream(workspace_bucket, file, chunk_size=8192))
    #
    tarinfo.size = size
    tf.addfile(tarinfo=tarinfo, fileobj=stream)

tf.close()