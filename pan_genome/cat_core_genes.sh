#!/bin/bash

for file in ../*.fasta
do
name=`basename $file`
echo '----'${name%.*}'-----'
cat all.faa|awk -v RS='>' "/${name%.*}/" |sed -e '/|/d' |tr -d '\n' |awk 'BEGIN {print "'">${name%.*}"'"}{print $0}' >${name%.*}.fna
done
