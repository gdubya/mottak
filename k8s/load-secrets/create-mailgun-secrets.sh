#!/bin/sh

kubectl create secret generic mailgun  \
--from-file=apiKey=./mailgun-apiKey \
--from-file=emailDomain=./mailgun-emailDomain
