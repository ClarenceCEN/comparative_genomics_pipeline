#!/bin/bash


for file in ./*.fna
do
name=`basename $file`

#/plus/work/soft/orthomclSoftware-v2.0.9/bin/orthomclAdjustFasta ${name%.*} ${name%.*}.faa 1
perl /plus/work/soft/genemark_suite_linux_64/gmsuite/gmsn.pl --prok --format GFF --fnn --faa ${name%.*}.fna

echo 'done!'
done
