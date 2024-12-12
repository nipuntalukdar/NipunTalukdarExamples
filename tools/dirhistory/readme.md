# A simple directory history tool

Here is a tool for you to remember the latest few directories that you were in a Linux machine. It works with the bash shell. 

All you need to do is:
```
# Go to home directory
cd 
# create directory .dirs in your home directory
mkdir .dirs

# then copy the files dirs.py  dirs.sh  dirs_show.py  dirsw.py to $HOME/.dirs
# Then execute the below command
soure $HOME/.dirs/dirs.sh

```

Now you will have a function xcd available for you.
If you want to remember some directory for future, you can do something like as shown below:

```
xcd  /path/to/some/dir
xcd /tmp
xcd $PWD

```

The above commands will cd to those directories as well as will remember them.
Now if you want to go to some directory in the remembered list, you may do the below:

```
#xcd dash dash
xcd --

#It will print a a list like the one shown below:

   1: /home/geet/vnf/datasets
   2: /home/geet
   3: /home/geet/test
   4: /home/geet/.dirs
   5: /tmp
   6: /home/geet/.kube

You may entter a number, or a directory path or simply enter nothing. 
If you just press enter (without any text), then it will cd to your home directory.

```

By default, xcd can remember last 20 directories. If you want to override that valule, you may do this:
```
export MAX_DIR_HISTORY=40
```
