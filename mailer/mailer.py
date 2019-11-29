#!/usr/bin/env python3
from __future__ import print_function   # for eprint
from __future__ import with_statement

import os
import sys
import logging
import requests
import glob

from dotenv import load_dotenv
load_dotenv()


def eprint(*args, **kwargs):
    """ Print to stderr """
    print(*args, file=sys.stderr, **kwargs)


def verify_environment():
    """Verify that the required environment variables are set.
    exits if is unhappy.
    """
    reqs = ['NAME', 'RECIPIENT', 'SUBJECT', 'MESSAGE',
            'MAILGUN_API_KEY', 'MAILGUN_DOMAIN']
    for req in reqs:
        if not os.getenv(req):
            logging.error('Environment variable ' + req + ' is not set')
            sys.exit(2)


def find_attachments(path):
    files = []
    if path and os.path.isdir(path):
        files = [f for f in glob.glob(path + "/*")]
        return(files)
    else:
        return(files)


def send_message(name, recipient, subject, message, attachments,verbose):
    if verbose:
        print(
            f"Sending message to '{name}' <{recipient}>\n",
            f"Subject is '{subject}'\n",
            f"Message is '{message}'\n",
            "Message has attachments\n" if attachments else "No attachments\n")
    ret = requests.post(
        "https://api.mailgun.net/v3/%s/messages" % os.getenv('MAILGUN_DOMAIN'),
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": "The Mailgun <donotreply@%s>" % os.getenv('MAILGUN_DOMAIN'),
              "to": [name, recipient],
              "subject": subject,
              "text": message},
        files=attachments)

    if verbose:
        print(f'Status: {ret.status_code}')
        print(f'Body:   {ret.text}')



# Check that we got what we need to run:
verify_environment()

# Map environment into Python:
recipient = os.getenv('RECIPIENT')
name = os.getenv('NAME')
message = os.getenv('MESSAGE')
subject = os.getenv('SUBJECT')
files = find_attachments(os.getenv('ATTACHMENTS'))


# Transform the file list into something like this:
#        files=[("attachment", ("test.jpg", open("files/test.jpg","rb").read())),
#               ("attachment", ("test.txt", open("files/test.txt","rb").read()))],
attachments = list(map(lambda f: (
    'attachment', (os.path.basename(f), open(f, "rb").read())), files))
send_message(recipient=recipient, name=name, subject=subject,
             message=message, attachments=attachments, verbose=True)

if __name__ == '__main__':
    if True:
        sys.exit(0)
    else:
        sys.exit(1)
