#!/usr/bin/env python3
import os
import sys
import logging

import tarfile
import ar_s3_helper as ar

import io
import csv

from dotenv import load_dotenv
load_dotenv()

global csv_list

"""
get_csv - fetch the list of files from the CSV ($uuid.csv)
and return it.
"""
def get_files(bucket, uuid):
    mylist = []
    csvobj = workspace_bucket.Object(key=f'{uuid}.csv')
    # S3 returns byte. We need text so we wrap it in StringIO
    csvbody = io.StringIO(csvobj.get()['Body'].read().decode('utf-8'))
    csvreader = csv.reader(csvbody, dialect='excel')
    # skip first row:
    csvreader.__next__()
    
    for row in csvreader:
        mylist.append(row[2])
    return mylist

"""
 We create our own file-like object to write binary data to 
 stdout
"""
class stdoutIO(io.BytesIO):
    def write(self, data):
        sys.stdout.buffer.write(data)
        return
        

bucket = os.getenv('BUCKET')
filename = os.getenv('OBJECT')
uuid = os.getenv('UUID')

s3 = ar.get_s3_resource()
workspace_bucket = s3.Bucket(os.getenv('WORKSPACE'))

csv_list = get_files(workspace_bucket, uuid)

# fp = os.fdopen(sys.stdout.fileno(), 'wb')
fp = stdoutIO()

tf = tarfile.open(fileobj=fp, mode='w|')
for file in csv_list:
    print(file)
    o = workspace_bucket.Object(key=file)
    tarinfo = tarfile.TarInfo(name=file)
    tarinfo.size = o.get()['ContentLength']
    tf.addfile(tarinfo=tarinfo, fileobj=o.get()['Body'])

tf.close()