#!/usr/bin/env python

import sys
from distlockcomm import DistLockComm

if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit(1)
    datareadlen = int(sys.argv[1])
    if datareadlen <= 0:
        datareadlen = 10000000
    p = DistLockComm()
    fin = open('out.dump', 'rb')
    if fin is None:
        print 'Could not open out.dump'
        exit(1)
    byte = None
    while True:
        byte = fin.read(datareadlen)
        if byte == '':
            break
        p.dataReceived(byte)
