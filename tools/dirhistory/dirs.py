import os
import sys

if len(sys.argv) < 2:
  print(os.getenv('HOME'))
  exit(0)
home=os.getenv('HOME')
dir_file=f'{home}/.dirs/dirs.txt'
dirwant = sys.argv[1]
dirwant = dirwant.strip()
try:
  with open(dir_file, 'r') as fp:
    dirs = fp.readlines()
    dirs=[d.strip() for d in dirs]
    try:
      offset = int(dirwant)
      offset = abs(offset)
      if offset <= len(dirs) and offset >= 1:
        dirwant = dirs[offset - 1]
    except ValueError:
      pass
    if not dirwant:
      print(os.getenv('HOME'))
    else:
      print(dirwant)
except:
  print(os.getenv('HOME'))
