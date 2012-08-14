===================================================================================================
===================================================================================================

This is a simple python example to do a very simple work. This is generally to address one of the
most boring part of our work. Generally we locate a file and do something with the file while doing
development. For example, we may have two/three locations in our machine where we maintain        
development directories. Generally, we do the following:                                          
    1. Locate the file                                                                            
    2. There may multiple copies of the file, but we want to do something with one copy of the file
    3. We select one copy of the file                                                             
    4. Then we may                                                                                
        - Edit the file                                                                           
        - Go to directory of the file and do something
        - Delete the file

This simple thing needs a lot of typing. This typing can be avoided by using this tool. I can write
a one line shell script to do the same. But I want to practice Python and Python is much more
powerful than simple shell scripts.

The tool uses 'locate' command to locate the file. 'locate' is part of mlocate package. On a CentOS
or Redhat Linux system, you may issue "yum search mlocate"  command to search mlocate package and
then "yum install" to install the package. If you have mlocate installed, run "updatedb" to have the
latest filenames in your system to mlocate database. mlocate stores the filenames in a Berkeley DB 
database and "locate" searches for the file name in this database. The DB may not be updated with 
the latest file names and so it is better to have a cron job runing every 4/5 hours to keep the DB
updated.

The script locates file(s) by its name and ask you to choose one of the matched file. Then it ask
you what you would like to do with the file. It allows 3 actions as given below:
    Choice <1> open the file with vim
    Choice <2> change directory to file location
    Choice <3> delete the file
Thats all.

Usage is given below:
findfileaction.py filename <regex> <filter-file-regex>

filename may be a regular expression and that is assumed if the 2nd command line argument is 
"regex". 2nd argument and 3rd argument are optional. 3rd argument is used to filter some file out.
E.g. if you don't want to see .cpp files, then pass '.*cpp$' as the 3rd argument. 3rd argument can
be a regular expression.

Hope the tool will be helpful for you :)

===================================================================================================
