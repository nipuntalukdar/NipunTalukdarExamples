import os
import sys
from gtts import gTTS

if len(sys.argv) < 3:
    print 'Exiting ...'
    sys.exit(1)

lines = None
with open(sys.argv[1], 'r') as fp:
    lines = fp.readlines()
    lines = [l.strip() for l in lines]

os.makedirs(sys.argv[2])
target = sys.argv[2]
i = 1
for l in lines:
    tts = gTTS(l)
    if l == '':
        continue
    tts.save('{}/{}.mp3'.format(target, i))
    i += 1
