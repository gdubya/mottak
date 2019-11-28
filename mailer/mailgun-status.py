#!/usr/bin/env python3

import requests
import os
from dotenv import load_dotenv
load_dotenv()


key = os.getenv('MAILGUN_API_KEY')
sandbox = os.getenv('MAILGUN_DOMAIN')

request_url = 'https://api.mailgun.net/v3/{0}/events'.format(sandbox)
request = requests.get(request_url, auth=('api', key), params={'limit': 5})

print(f'Status: {request.status_code}')
print(f'Body:   {request.text}')