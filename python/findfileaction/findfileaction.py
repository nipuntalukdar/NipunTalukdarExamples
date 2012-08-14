#!/usr/bin/python

import sys
import string
import subprocess
import re
import os

def delete_file(filename):
    if (not os.path.isfile(filename)):
        print filename + " seems not there or not a rgular file"
        return False
    os.remove(filename)
    return True


def open_file_with_vim(filename):
    if (not os.path.isfile(filename)):
        print filename + " seems not there "
        return False
    subprocess.call(['vim' , filename])
    return True

def cd_to_dir(filename):
    cdloc = ''
    if (os.path.isdir(filename)):
        cdloc = filename
    elif (os.path.isfile(filename)):
        cdloc = os.path.dirname(filename)
    else:
        print filename + ' might not exist'
        return False
    os.chdir(cdloc)
    subprocess.call([os.getenv('SHELL') ])
    return True
    
def read_choie(prompt, max_val, min_val, bad_choice):
    try:
        x = raw_input(prompt);
        if (int(x) > max_val):
            return bad_choice
        return x
    except ValueError:
        return bad_choice

def find_file(filename, regexex=False):
    output = ""
    if (regexex == False):
        output = subprocess.Popen(['locate' , filename ] , stdout=subprocess.PIPE ).communicate()[0]
    else:
        output = subprocess.Popen(['locate' , '-r', filename ] , stdout=subprocess.PIPE ).communicate()[0]
    files = string.split(output, '\n')
    return files
try: 
    regexex = False
    filterexp = None
    if ((len(sys.argv) > 2) and (sys.argv[2].lower() == 'regex' )):
        regexex = True
    if (len(sys.argv) > 3):
        filterexp = re.compile(sys.argv[3]) 
    files = find_file(sys.argv[1], regexex )
    required_files = []
    printname=False
    for file in files:
        printname = True
        if ((filterexp is not None)and (filterexp.search(file) is not None)):
            printname = False
        if ( printname  and file != "") :
            required_files.append(file)
    i = 0
    for file in required_files:
        print str(i) + "  " + file
        i = i + 1
    if (len(required_files) == 0):
        sys.exit(0)
    bad_choice = 4294967295
    choice_index = read_choie('Please index of your file of interest ', len(required_files) -1,\
            0, bad_choice)
    if (choice_index == bad_choice):
        print "You chose bad index"
        sys.exit(1)
    print "What you want to do with this file "
    print "Choice <1> open the file with vim "
    print "Choice <2> change directory to file location "
    print "Choice <3> delete the file "
    
    work_index = read_choie('Please enter your choice ', 3, 1, bad_choice)
    if (work_index == bad_choice):
        print "Bad choice"
        sys.exit(1)
    if (work_index == '1'):
        open_file_with_vim(required_files[int(choice_index)])
    elif (work_index == '2'):
            cd_to_dir(required_files[int(choice_index)])
    elif (work_index == '3'):
            delete_file(required_files[int(choice_index)])
    sys.exit(0)

except IndexError:
    print 'Usage: ' + sys.argv[0] + " filename <regex> <filter-file-regex> "

