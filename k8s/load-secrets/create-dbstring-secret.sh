#!/bin/sh

echo loading the content of the file dsn into the secret.
echo it should look like this:
echo "pgsql:host=10.0.0.1;dbname=mottak;user=mottak;password=verysecret"

kubectl -n argo delete secret invitation-dsn
kubectl -n argo delete secret log-dsn

kubectl -n argo create secret generic invitation-dsn --from-file=invitation-dsn
kubectl -n argo create secret generic log-dsn --from-file=log-dsn

