#!/bin/sh
kubectl -n argo create secret tls tls-mottak-ingress --cert=mottak_arkivverket_dev.pem --key=mottak_arkivverket_dev.key
