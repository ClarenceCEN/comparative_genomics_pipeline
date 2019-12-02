#!/bin/bash


for file in ./*.faa
do
name=`basename $file`

/plus/work/soft/orthomclSoftware-v2.0.9/bin/orthomclAdjustFasta ${name%.*} ${name%.*}.faa 1

echo 'done!'
done
