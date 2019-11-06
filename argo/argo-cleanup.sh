#!/bin/sh

argo list | awk '{ print $1}'|grep -v NAME|xargs -n1 argo delete
