#!/bin/sh

kubectl -n argo create secret generic route53-cred  --from-file=accessKeySecret=./route53-accessKeySecret --from-file=secretKeySecret=./route53-secretKeySecret

