#!/usr/bin/python

import sys
from os.path import basename
import json
import requests
from getpass import getpass

GISTAPI_URL = 'https://api.github.com/gists'
user = 'nipuntalukdar'
password = ''
description = 'Simple example'

if len(sys.argv) < 2:
    usage = '''
        Please pass the file you want to gist
        i.e.
        $ python {} <filepath>
    '''
    u = usage.format(sys.argv[0])
    print(u)
    sys.exit(1)
try:
    user = raw_input('User: ')
    description = raw_input('Description: ')
except NameError:
    user = input('User: ')
    description = raw_input('Description: ')
password = getpass()

file_content = None
with open(sys.argv[1], 'r') as fp:
    file_content = fp.read()

data = { 
    'description' : description,
    'public' : True,
    'files' : {
        basename(sys.argv[1]): {
            'content' : file_content
        }
    }
}

headers = {'content-type' : 'raw/json'}
gistr = requests.post(GISTAPI_URL, data=json.dumps(data), auth=(user, password), headers=headers)
if gistr.status_code == 200 or gistr.status_code == 201 :
    print('Gist created or updated')
else:
    print('Failed', gistr.status_code)

