#!/usr/bin/env python
import logging
import io
import os

import subprocess
from av_objectstore import ArkivverketObjectStorage

from dotenv import load_dotenv
load_dotenv()

class SimpleIterator:
    def __init__(self, it):
        self.it = it
        
    def __iter__(self):
        return self.it.__iter__()

    def __next__(self):
        return self.it.__next__()


uuid     = os.getenv('UUID')
filename = f'{uuid}.1.tar'  # target.

bucket   = os.getenv('BUCKET')

storage  = ArkivverketObjectStorage()

pipe = subprocess.Popen(['./generate-tar.py'], bufsize=0, shell=False, stdin=None, text=None,
                             stdout=subprocess.PIPE, env=os.environ)

return_code = pipe.poll()

myit = SimpleIterator(iter(pipe.stdout)) # stupid libcloud thinks it can seek on the iterator.

while return_code is None:
    ret = storage.upload_stream(container=bucket, name=filename, iterator=myit)
    return_code = pipe.poll()

