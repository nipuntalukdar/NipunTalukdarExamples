#!/usr/bin/python                         
# save the code below in a file named filehandler.py 
import glob                                          
import hashlib                                       
import os                                            
import sys                                           
import re                                            
from collections import deque                        

class unique_file_checker:
    def __init__(self):   
        self.elems = {}   
        self.futil = file_util('.')

    def add_file(self, file): 
        md5val = self.futil.file_checksum(file)
        if (md5val in self.elems ):            
            del self.elems[md5val]             
            return                             
        self.elems[md5val] = file              

    def print_unique_files(self):
        for k,v in self.elems.iteritems():
            print k + ' ' + v             

    def get_unique_files(self):
        unique_files = set()   
        for k,v in self.elems.iteritems():
            unique_files.add(v)           
        return unique_files               

class compare_directory:
    def __init__(self, dir1, dir2):
        self.elems = {}            
        self.dir1 = dir1           
        self.dir2 = dir2           

    def add_file(self, dirspec , relativefile, hash):
        if dirspec != self.dir1 and dirspec != self.dir2:
            return                                       
        if relativefile in self.elems :                  
           if dirspec in self.elems[relativefile]:       
               return                                    
           otherelem = None                              
           if dirspec == self.dir1:                      
               otherelem = self.dir2                     
           else:                                         
              otherelem = self.dir1                      
           if self.elems[relativefile][otherelem] == hash:
              del self.elems[relativefile]                
           else:                                          
              self.elems[relativefile][dirspec] = hash    
        else:                                             
            self.elems[relativefile] = {dirspec : hash}   

    def get_diff_files(self):
        if  0 == len(self.elems):
            return               
        # Now split the dictinary into 3 dictionary
        inboth = set()                             
        infirst = set()                            
        insecond = set()                           
        for relativefile in self.elems:            
            values = self.elems[relativefile]      
            if len(values) == 2:                   
                inboth.add(relativefile)           
            elif self.dir1 in values:              
                infirst.add(relativefile)          
            else:                                  
                insecond.add(relativefile)         
        return infirst, insecond, inboth           

class file_util:
    def __init__(self, rootdir):
        self.root = rootdir     
    def scandir(self, dir = ''):
        scandir = self.root     
        if (dir != ''):         
            scandir = dir       
        # Now get all the contents of the directory
        filelist = glob.glob(scandir + '/*')       
        return filelist                            

    def file_checksum(self, filename):
        f = open(filename, 'r')       
        if (f != None) :              
            x = f.read()              
            md5 = hashlib.md5()       
            md5.update(x)             
            f.close()                 
            return md5.hexdigest()    
        return 0                      

class directory_scanner:
    def __init__(self, rootdir):
        self.root = rootdir     
        self.filter = set()     
        self.acceptfilter = set()
        self.acceptlen = 0       

    def set_root_dir(self, rootdir):
        self.root = rootdir         

    def add_reject_filter(self, filterexpr):
        self.filter.add(filterexpr)         

    def add_accept_filter(self, filterexpr):
        self.acceptfilter.add(filterexpr)   
        self.acceptlen = len(self.acceptfilter)

    def accept_file(self, thisfile):
        if (0 == self.acceptlen):   
            return True             
        for fltr in self.acceptfilter:
            if (re.search(fltr, thisfile)):
                return True                
        return False                       

    def filter_file(self, thisfile):
        for fltr in self.filter:    
            if (re.search(fltr, thisfile)):
                return True                
        return False                       

    def get_file_list(self, excludedir):
        dirs = deque()                  
        fileset = set()                 
        dirs.append(self.root)          
        dirstrlen = len(self.root)

        try:
            while True:
                scandir = dirs.pop()
                filelist = glob.glob(scandir + '/*')

                for thisfile in filelist:
                    if (self.filter_file(thisfile)):
                        continue

                    if (os.path.isdir(thisfile)) :
                        if (False == excludedir):
                            fileset.add(thisfile)
                        dirs.append(thisfile)
                        continue

                    if (False == self.accept_file(thisfile)):
                        continue

                    if (not os.path.isfile(thisfile)):
                        continue
                    # remove the dirname prefix from the files
                    index = thisfile.find(self.root)
                    if (index != -1 and len(thisfile) > (index + dirstrlen)):
                        thisfile = thisfile[index + dirstrlen + index:]
                    fileset.add(thisfile)
        except IndexError:
            return fileset
        return fileset
