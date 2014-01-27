#!/usr/bin/python
import os
import sys
from filehandler import directory_scanner

dirtoscan = '.'
if (len(sys.argv) > 1):
    dirtoscan = sys.argv[1]

if  (not os.path.isdir(dirtoscan)):
    sys.exit(1)
a = directory_scanner(dirtoscan)
x = a.get_file_list(False)
for a in x:
    print a
