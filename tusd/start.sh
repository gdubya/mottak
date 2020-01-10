#!/bin/bash
# clean up endpoint
MY_ENDPOINT=$(echo $ENDPOINT|sed 's,https://,,g')

TUSD_PARAMS="--hooks-dir /sr/tusd-hooks --behind-proxy --s3-bucket $BUCKET --s3-endpoint $MY_ENDPOINT"
echo tusd command line: tusd $TUSD_PARAMS
tusd $TUSD_PARAMS

