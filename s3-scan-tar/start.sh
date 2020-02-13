#!/bin/sh
echo Starting ClamAV
/usr/sbin/clamd
echo Initializing scan...
/opt/s3-scan-tar.py
