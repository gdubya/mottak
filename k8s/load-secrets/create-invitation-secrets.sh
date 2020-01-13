#!/bin/sh

kubectl -n argo create secret generic invitation  \
--from-file=applicationSecret=./invitation-applicationSecret
