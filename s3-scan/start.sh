#!/bin/sh
/usr/sbin/clamd && /opt/s3-avscan.py
RV=$?
cat /tmp/av.log
exit $RV