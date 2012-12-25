#!/bin/bash

TAR=`which tar`
MANDIR=/usr/share/man/man3

for f in $(ls *.tar.gz); do
	${TAR} --no-same-owner --directory=${MANDIR} -xvzf ${f}
done
