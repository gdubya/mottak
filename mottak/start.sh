#!/bin/sh

php /srv/app/reactor migrate.up && php /srv/app/reactor server
