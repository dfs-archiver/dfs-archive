#!/bin/bash
DOMAIN="www.itsdougholland.com"
wget \
  --recursive \
  --level 5 \
  --no-clobber \
  --page-requisites \
  --adjust-extension \
  --span-hosts \
  --convert-links \
  --restrict-file-names=windows \
  --domains $DOMAIN \
  --no-parent \
  --exclude-directories "/feeds" \
  --reject "*@showComment*" \
  $DOMAIN
# --execute robots=off \
./done.sh
