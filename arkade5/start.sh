#!/bin/sh -e

echo Fetching via s3


# transform endpoint (URL) to hostname
host=$(echo $ENDPOINT|sed 's,https://,,g')
basename=$(basename -s .tar $OBJECT)

cd /opt
mkdir input output tmp
cd input
s3cmd get --access_key $AWS_ACCESS_KEY_ID --secret_key $AWS_SECRET_ACCESS_KEY --host-bucket $host --host $host s3://$BUCKET/$OBJECT

# Hent ut METS-fil fra tarballen:
tar xf $OBJECT "$basename/dias-mets.xml"

# Arkade får spader om vi ikke er i samme katalog.
cd /opt/Arkade5CLI-1.5.0



./arkade.sh -a /opt/input/$OBJECT -p /opt/tmp -o /opt/output -s packing -m /opt/input/$basename/dias-mets.xml -t noark5
