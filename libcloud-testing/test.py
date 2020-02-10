#!/usr/bin/env python

from av_objectstore import ArkivverketObjectStorage
import os

import string
import random
from dotenv import load_dotenv
load_dotenv()

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

name = randomString()

storage = ArkivverketObjectStorage()

list = iter([b"foo.", b"bar.", b"baz.", b"quux."])
print("Streaming upload....")
storage.upload_stream(container='av-workspace', name=name, iterator=list)
print("Download....")
storage.download_file('av-workspace', name, name)
print("Delete...")
storage.delete('av-workspace', name)
print("Upload")
storage.upload_file(container='av-workspace', name=name, file=name)
print("Streaming download")
stream = storage.download_stream('av-workspace', name)
for chunk in stream:
    print(chunk)
print("Listing content")

foo = storage.list_container('av-workspace')
print("Number of objects in storage:", len(foo))
print("Deleting again")
storage.delete('av-workspace', name)
