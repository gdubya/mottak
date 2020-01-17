#!/bin/sh

# secrets are stored in two files
# accessKeySecret - the AWS key
# secretKeySecret - the AWS secret key
kubectl -n argo delete secret s3-cred
kubectl -n argo create secret generic s3-cred  --from-file=accessKeySecret=./s3-accessKeySecret --from-file=secretKeySecret=./s3-secretKeySecret

