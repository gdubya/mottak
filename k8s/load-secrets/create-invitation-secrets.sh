#!/bin/sh

kubectl create secret generic invitation  \
--from-file=applicationSecret=./invitation-applicationSecret
