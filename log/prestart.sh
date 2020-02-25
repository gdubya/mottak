#!/bin/sh
echo Applying Yoyo migrations.
yoyo apply --no-config-file --database $DSN --batch app/migrations
echo done.