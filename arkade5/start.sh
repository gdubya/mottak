#!/bin/sh -e

echo Fetching via s3

echo Using $AWS_ACCESS_KEY_ID fetch via s3
echo Endpoint: $ENDPOINT
echo Object: $OBJECT


# transform endpoint (URL) to hostname
# Note that S3 will break if there is a trailing slash.
# Todo: create a sed expressions that cleans better.
host=$(echo $ENDPOINT|sed 's,https://,,g')
basename=$(basename -s .tar $OBJECT)

cd /opt
mkdir input output tmp
cd input
# Add --debug after s3cmd to debug S3-related issues.
s3cmd --access_key $AWS_ACCESS_KEY_ID --secret_key $AWS_SECRET_ACCESS_KEY --host-bucket $host --host $host s3://$BUCKET/$OBJECT

# Hent ut METS-fil fra tarballen:
tar xf $OBJECT "$basename/dias-mets.xml"


# kjør arkade direkte 
dotnet /opt/Arkade5CLI-1.5.0/Arkivverket.Arkade.CLI.dll -a /opt/input/$OBJECT -p /opt/tmp -o /opt/output -s packing -m /opt/input/$basename/dias-mets.xml -t noark5

# The report is available at /opt/output/Arkaderapport-$basename.html
# Move it to a know location so Argo can get at it.
mv /opt/output/Arkaderapport-$basename.html /tmp/arkade.html
