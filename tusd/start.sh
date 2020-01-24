#!/bin/bash
# clean up endpoint
MY_ENDPOINT=$(echo $ENDPOINT|sed 's,https://,,g')
echo "Endpoint transformation: $ENDPOINT --> $MY_ENDPOINT"
OPT_PARAMS=""

# Handle optional configuration from environment:
if [ -n "$BASE_PATH" ]; then
    OPT_PARAMS="$OPT_PARAMS --base-path $BASE_PATH"
fi
# Pick between GCS and S3
if [ -n "$GCS_SERVICE_ACCOUNT_FILE" ]; then
    echo "Assuming we're using the GCS native backend."
    if [ ! -a $GCS_SERVICE_ACCOUNT_FILE ]; then
        echo "Warning: $GCS_SERVICE_ACCOUNT_FILE doesn't seem to exists. Things will likely fail."
    fi
    TUSD_PARAMS="--hooks-dir /srv/tusd-hooks --behind-proxy --gcs-bucket $BUCKET"
else
    echo "Assuming we're using the S3 backend"
    TUSD_PARAMS="--hooks-dir /srv/tusd-hooks --behind-proxy --s3-bucket $BUCKET --s3-endpoint $MY_ENDPOINT"
fi

echo tusd command line: "tusd $TUSD_PARAMS $OPT_PARAMS"
tusd $TUSD_PARAMS $OPT_PARAMS

