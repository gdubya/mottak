#!/bin/sh
. /etc/secrets/dsn/dsn

echo DSN: $dsn

php /srv/app/reactor migrate.up

apache2-foreground
