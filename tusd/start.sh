#!/bin/bash
# clean up endpoint
OPT_PARAMS=""

# Handle optional configuration from environment:
if [ -n "$BASE_PATH" ]; then
    OPT_PARAMS="$OPT_PARAMS --base-path $BASE_PATH"
fi

# pick GCS:
if [ "$OBJECTSTORE" == "gcs" ]; then
    echo "Backend is GCS (bucket: $BUCKET). Setting GCS_SERVICE_ACCOUNT_FILE to $AUTH_TOKEN"
    export GCS_SERVICE_ACCOUNT_FILE=$AUTH_TOKEN
    TUSD_PARAMS="--hooks-dir /srv/tusd-hooks --behind-proxy --gcs-bucket $BUCKET"
# handle Azure here if we're supporting it:
else
    echo "Assuming we're using the S3 backend"
    TUSD_PARAMS="--hooks-dir /srv/tusd-hooks --behind-proxy --s3-bucket $BUCKET --s3-endpoint $ENDPOINT"
fi

echo tusd command line: "tusd $TUSD_PARAMS $OPT_PARAMS"
tusd $TUSD_PARAMS $OPT_PARAMS

