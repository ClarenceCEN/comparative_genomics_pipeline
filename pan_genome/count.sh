#!/bin/bash


for file in ./*.tab
do
name=`basename $file`
echo '----'${name%.*}'-----'
python cal.py ${name%.*}

done
