#!/bin/bash

file_name=''
for file in ./input/*.function
do
name=`basename $file`
file_name=${file_name}"+"${name%.*}
done
echo $file_name