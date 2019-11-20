#!/bin/sh
# . /etc/secrets/dsn/dsn

# echo DSN: $DBSTRING

php /srv/app/reactor migrate.up

apache2-foreground
