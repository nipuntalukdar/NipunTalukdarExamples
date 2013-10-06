"""
This program is an example demonstrating finding duplicate files across many
diirectories. At the end it print out list of duplicate files in the
directories.

Run this program is as shown below:
    $ python duplicate_file_finder.py dir1 dir2 dir3 dir4 .....
    Eg.
        $ python duplicate_file_finder.py dir1  /test1 /test2

Author: Nipun Talukdar

"""
import os
import sys
import glob                                          
import hashlib                                       

def file_checksum(filename):
    f = open(filename, 'r')       
    if (f != None) :              
        x = f.read()              
        md5 = hashlib.md5()       
        md5.update(x)             
        f.close()                 
        return md5.hexdigest()    
    return 0                      

def get_regular_files(dirname, regular_files):
    dirlist = []
    try:
        files = os.listdir(dirname)
        for fname in  files:
            realpath = dirname + '/' + fname
            if os.path.isfile(realpath):
                regular_files.append(realpath)
            elif os.path.isdir(realpath):
                dirlist.append(realpath)
    except OSError as oe:
        pass
    for dirfound in dirlist:
        get_regular_files(dirfound, regular_files)

if len(sys.argv) > 1:
    dirs = set()
    i = 1
    while i  < len(sys.argv):
        dirs.add(sys.argv[i])
        i = i + 1
    regfiles = [] 
    for dir in dirs:
        get_regular_files(dir , regfiles)
    
    checksum_list = {}
    for fpath in regfiles:
        checksum = file_checksum(fpath)
        if checksum not in checksum_list:
            checksum_list[checksum] = []
        checksum_list[checksum].append(fpath)
    i = 1
    for checksum in checksum_list:
        if len(checksum_list[checksum]) > 1:
            print 'Duplicate list ' + str(i) 
            for fpath in checksum_list[checksum]:
                print fpath
            print '------\n-----'
            i = i + 1
