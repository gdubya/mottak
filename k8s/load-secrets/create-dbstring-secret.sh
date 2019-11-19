#!/bin/sh

echo We're loading the content of the file dsn into the secret.
echo it should look like this:
echo pgsql:host=10.0.0.1;dbname=mottak;user=mottak;password=verysecret
 
kubectl create secret generic dsn --from-file=dsn
