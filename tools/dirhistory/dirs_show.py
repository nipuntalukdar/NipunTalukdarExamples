import os
home=os.getenv('HOME')
dir_file=f'{home}/.dirs/dirs.txt'
try:
  with open(dir_file, 'r') as fp:
    dirs = fp.readlines()
    dirs=[d.strip() for d in dirs]
    j = 1
    for i in dirs:
      print('%4d: %s' % (j, i))
      j += 1
except:
  pass
