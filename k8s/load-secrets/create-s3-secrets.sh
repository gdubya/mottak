#!/bin/sh

# secrets are stored in two files
# accessKeySecret - the AWS key
# secretKeySecret - the AWS secret key

kubectl create secret generic s3-cred  --from-file=accessKeySecret=./accessKeySecret --from-file=secretKeySecret=./secretKeySecret

