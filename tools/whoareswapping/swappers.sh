#!/bin/bash

regex='^[0-9]+$'
rm -f /tmp/helloswapersxxx
for i in `ls /proc`
do
    if [ ! -d /proc/$i ] ; then
        continue
    fi
    if  [[ $i =~ $regex ]] ; then
        x=`grep VmSwap /proc/$i/status`
        if [ $? -ne 0 ] ; then
            continue
        fi
        y="$x $i"
        y=`echo $y | sed 's/VmSwap: //'`
        echo $y >> /tmp/helloswapersxxx
    fi
done
cat /tmp/helloswapersxxx | sort -nr
rm /tmp/helloswapersxxx
