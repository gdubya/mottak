#!/bin/bash
echo tusd command line: tusd --hooks-dir /srv/tusd-hooks --behind-proxy --gcs-bucket $BUCKET
tusd --hooks-dir /srv/tusd-hooks --behind-proxy --gcs-bucket $BUCKET

