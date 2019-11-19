#!/bin/sh

echo Looking for gcs.json. Will create the k8s secret gcs-cred which will contain the file
echo in the container it will be available according to the deployment.

kubectl create secret generic gcs-cred  --from-file=gcs.json
