import os
import sys
DEFAULT_MAX_HISTORY=20

if len(sys.argv) < 2:
  exit(0)
add_dir = sys.argv[1]
dirs = []
max_dirs=os.getenv('MAX_DIR_HISTORY', DEFAULT_MAX_HISTORY)
try:
  max_dirs = abs(int(max_dirs))
except:
  max_dirs = DEFAULT_MAX_HISTORY
if max_dirs == 0:
  max_dirs = DEFAULT_MAX_HISTORY
home=os.getenv('HOME')
dir_file=f'{home}/.dirs/dirs.txt'
try:
  with open(dir_file, 'r') as fp:
    dirs_t = fp.readlines()
    dirs_t=[d.strip() for d in dirs_t]
    dirs = dirs_t
except:
  pass

if add_dir in dirs:
  dirs.remove(add_dir)
dirs.insert(0, add_dir)
if len(dirs) > max_dirs:
  dirs=dirs[:max_dirs]

file_out = '\n'.join(dirs) + '\n'
with open(dir_file, 'wt') as fp:
  fp.write(file_out)



