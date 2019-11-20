import argparse
import base64
import json
import uuid

parser = argparse.ArgumentParser(description='Build a Uploader URL for testing.')

parser.add_argument('-u', '--upload-url', type=str, required=True, help='The tusd endpoint URL')
parser.add_argument('-i', '--invitation-id', type=int, required=True, help='The invitation id')

args = parser.parse_args()

url = {
    'reference': str(uuid.uuid4()),
    'uploadUrl': args.upload_url,
    'uploadType': 'tar',
    'meta': {
        'invitation_id': args.invitation_id,
    },
}

print('dpldr://%s' % (base64.b64encode(json.dumps(url))))
