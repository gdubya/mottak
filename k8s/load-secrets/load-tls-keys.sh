#!/bin/sh
kubectl -n argo delete secret tls-mottak-ingress
kubectl -n argo create secret tls tls-mottak-ingress \
--cert=star_mottak_arkivverket_dev.pem --key=star_mottak_arkivverket_dev.key
