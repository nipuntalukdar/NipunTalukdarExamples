#!/bin/bash

# This scripts changes the permission of all the directories
# under a certain directory to 0755
#

if [ $# -le 0 ] ; then 
    echo "Usage:  " $0  " start-directory "
    exit 1
fi
if [ ! -d $1 ] ; then
    echo "$1 is not a directory "
    exit 1
fi

for i in `find $1 -name "*" `
do
    if  [ -d $i ] ; then
        if [ $i == "." ] ; then
            continue
        fi
        if [ $i == ".." ] ; then
            continue
        fi
        echo $i
    fi
done

