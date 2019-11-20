#!/bin/sh -e

echo Fetching via s3

echo Using $AWS_ACCESS_KEY_ID fetch via s3
echo Endpoint: $ENDPOINT
echo Object: $OBJECT
echo Archieve type: $ARCHIEVE_TYPE


# transform endpoint (URL) to hostname
# Note that S3 will break if there is a trailing slash.
# Todo: create a sed expressions that cleans better.
host=$(echo $ENDPOINT|sed 's,https://,,g')
basename=$(basename -s .tar $OBJECT)

mkdir -p /opt
cd /opt
mkdir input output tmp
cd input
# Add --debug after s3cmd to debug S3-related issues.
s3cmd get \
     --access_key $AWS_ACCESS_KEY_ID \
     --secret_key $AWS_SECRET_ACCESS_KEY \
     --host-bucket $host --host $host s3://$BUCKET/$OBJECT

#run siegfried on package
sf -csv -z /opt/input/$OBJECT | /tmp/sf-output.csv
