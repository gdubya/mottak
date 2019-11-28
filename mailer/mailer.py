#!/usr/bin/env python3
from __future__ import print_function   # for eprint
from __future__ import with_statement

import os
import sys
import logging
import requests

from dotenv import load_dotenv
load_dotenv()


def eprint(*args, **kwargs):
    """ Print to stderr """
    print(*args, file=sys.stderr, **kwargs)


def verify_environment():
    """Verify that the required environment variables are set.
    exits if is unhappy.
    """
    reqs = ['RECIPIENT', 'SUBJECT', 'MESSAGE',
            'MAILGUN_API_KEY', 'MAILGUN_DOMAIN']
    for req in reqs:
        if not os.getenv(req):
            logging.error('Environment variable ' + req + ' is not set')
            sys.exit(2)


def send_simple_message():
    ret = requests.post(
        "https://api.mailgun.net/v3/%s/messages" % os.getenv('MAILGUN_DOMAIN'),
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": "The Mailgun <donotreply@%s>" % os.getenv('MAILGUN_DOMAIN'),
              "to": ["", os.getenv('RECIPIENT')],
              "subject": os.getenv('SUBJECT'),
              "text": os.getenv('MESSAGE')})
    print(f'Status: {ret.status_code}')
    print(f'Body:   {ret.text}')

verify_environment()
print("Mailing....")
send_simple_message()

if __name__ == '__main__':
    if True:
        sys.exit(0)
    else:
        sys.exit(1)
