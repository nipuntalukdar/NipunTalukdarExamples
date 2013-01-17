#!/usr/bin/python                               
import sys                                      
import os                                       
from filehandler import directory_scanner, unique_file_checker

if (len(sys.argv) < 2 ) :
        print "Usage :" + sys.argv[0] + " directory_1 directory_2 .... "
        sys.exit(1)                                                     

start = 1
dirlist = set()
while ( start < len(sys.argv)) :
        if (os.path.isdir(sys.argv[start]) and (sys.argv[start] not in dirlist) ):
                dirlist.add(sys.argv[start]);                                     
        start += 1                                                                

if (len(dirlist) == 0):
        print "None of the inputs were valid directories , hence exiting...."
        sys.exit(1)                                                          

dirsc = directory_scanner('.')
### reject files from SCCS directory, and files with extns .o. Accept files with
### .cc,.cpp,.c,.h,.hpp,.mk, Makefile for uniqueness checking

dirsc.add_reject_filter('SCCS')
dirsc.add_reject_filter('\.o$')
dirsc.add_reject_filter('\.pyc$')

dirsc.add_accept_filter('\.py$')
dirsc.add_accept_filter('\.cpp$')
dirsc.add_accept_filter('\.cc$')
dirsc.add_accept_filter('\.h$')
dirsc.add_accept_filter('\.hpp$')
dirsc.add_accept_filter('\.mk$')

u_checker = unique_file_checker()

for thisdir in dirlist:
        dirsc.set_root_dir(thisdir)
        filelist = dirsc.get_file_list(True)
        for thisfile in filelist:
                u_checker.add_file(thisdir + thisfile)

# Now get the unique file list

unique_files = u_checker.get_unique_files()

# Print the list of unique files
for unique_file in unique_files:
        print unique_file

sys.exit(0)
