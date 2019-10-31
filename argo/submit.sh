#!/bin/sh
echo Submitting Argo workflow $1 with parameters from env file
argo submit --watch $(for line in $(cat .env);do echo "--parameter $line";done) $1

