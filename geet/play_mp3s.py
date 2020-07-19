import sys
import os
from time import sleep, time
from subprocess import Popen
import subprocess
from random import randint
from copy import copy

if len(sys.argv[1]) < 2:
    print('Exiting....')
    sys.exit(1)
delaygiven = 4
if len(sys.argv) > 2:
    delaygiven = float(sys.argv[2])

playsequentially = False
if len(sys.argv) > 3:
    playsequentially = True
target = sys.argv[1]
files = os.listdir(target)
files = ['{}/{}'.format(target, f) for f in files]

player = '/usr/bin/mplayer'

def play_sequentially(mp3s, delay):
    mp3s.sort()
    count = len(mp3s)
    playidx = 0
    while True:
        if playidx == count:
            playidx = 0
        start = time()
        selected = mp3s[playidx]
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
        playidx += 1


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


if not playsequentially:
    playfiles(files, delaygiven)
else:
    play_sequentially(files, delaygiven)
