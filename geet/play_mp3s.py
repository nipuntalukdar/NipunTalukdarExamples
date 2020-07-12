import sys
import os
from time import sleep, time
from subprocess import Popen
import subprocess
from random import randint
from copy import copy

if len(sys.argv[1]) < 2:
    print 'Exiting....'
    sys.exit(1)
delaygiven = 4
if len(sys.argv) > 2:
    delaygiven = float(sys.argv[2])
target = sys.argv[1]
files = os.listdir(target)
files = ['{}/{}'.format(target, f) for f in files]

player = '/usr/bin/mplayer'

def playfiles(mp3s, delay):
    count = len(mp3s)
    tempmp3s1 = copy(mp3s)
    while True:
        if not tempmp3s1:
            tempmp3s1 = copy(mp3s)
        count = len(tempmp3s1)
        indx = randint(0, count -1)
        selected = tempmp3s1.pop(indx)
        start = time()
        p = Popen([player, selected],  stdout=subprocess.PIPE,
            stderr= subprocess.STDOUT)
        p.communicate()
        p.wait()
        current = time() - start
        actdelay = delay - current
        '''
        if actdelay > 0:
            sleep(actdelay)
        '''
        sleep(delay)

playfiles(files, delaygiven)
