#/usr/bin/python                       
import sys                             
import os                              
from filehandler import directory_scanner, compare_directory, file_util

if (len(sys.argv) != 3 or (sys.argv[1] == sys.argv[2]) or ( not os.path.isdir(sys.argv[1]) ) \
        or (not os.path.isdir(sys.argv[2] ))):                                                
        print "#### Usage: " + sys.argv[0] + " first_dir  second_dir"                         
        print "#### I compare two directories, exiting... "                                   
        sys.exit(1)                                                                           


dirsc = directory_scanner(sys.argv[1])

### reject files from SCCS directory, and files with extns .o. Accept files with
### .cc,.cpp,.c,.h,.hpp,.mk, Makefile for comparison                            

dirsc.add_reject_filter('SCCS')
dirsc.add_reject_filter('\.o$')
dirsc.add_reject_filter('\.pyc$')

dirsc.add_accept_filter('\.py$')
dirsc.add_accept_filter('\.cpp$')
dirsc.add_accept_filter('\.cc$') 
dirsc.add_accept_filter('\.h$')  
dirsc.add_accept_filter('\.hpp$')
dirsc.add_accept_filter('\.mk$') 


fileset1 =  dirsc.get_file_list(True)

dirsc.set_root_dir(sys.argv[2])
fileset2 = dirsc.get_file_list(True)

filediff = compare_directory(sys.argv[1], sys.argv[2])
fhnd = file_util('.')
for file_name in fileset1:
    hash_val = fhnd.file_checksum(sys.argv[1] + file_name)
    filediff.add_file(sys.argv[1], file_name,  hash_val)
for file_name in fileset2:
    hash_val = fhnd.file_checksum(sys.argv[2] + file_name)
    filediff.add_file(sys.argv[2], file_name,  hash_val)
(infirstonly, insecondonly, inbothbutdiffer) = filediff.get_diff_files()

#Print the name of the files found in first dir only
for thisfile in infirstonly:
        print "In " + sys.argv[1] + " only " + sys.argv[1] + thisfile

print "****************************"

#Print the name of the files found in second dir only
for thisfile in insecondonly:
        print "In " + sys.argv[2] + " only " + sys.argv[2] + thisfile

print "****************************"

#Print the name of the files found in first dir only
for thisfile in inbothbutdiffer:
        print "Found in both but differs (" + sys.argv[1] + "|" + sys.argv[2] + ")" + thisfile

print "****************************"
sys.exit(0)
