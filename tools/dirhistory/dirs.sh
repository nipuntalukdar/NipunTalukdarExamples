#!/usr/bin/bash
function xcd
{
  if [ $# -eq 0 ] ; then
    cd
    python $HOME/.dirs/dirsw.py $PWD  
    return 
  fi
  if [ $1 == "--" ] ; then
     if [ -f $HOME/.dirs/dirs.txt ] ; then
        python $HOME/.dirs/dirs_show.py
        read dirchoice
        if [ "x$dirchoice" = "x" ] ; then
          cd
          python $HOME/.dirs/dirsw.py $PWD
          return
        fi
        xyz=$(python $HOME/.dirs/dirs.py $dirchoice)
        cd $xyz
        if [ $? -eq 0 ] ; then
          python $HOME/.dirs/dirsw.py $PWD  
        fi
     else
        cd
        python $HOME/.dirs/dirsw.py $PWD
     fi
  else
     cd $1
     if [ $? -eq 0 ] ; then
        python $HOME/.dirs/dirsw.py $PWD
     fi
  fi
}
