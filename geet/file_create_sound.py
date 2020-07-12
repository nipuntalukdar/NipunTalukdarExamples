import os
import sys
from gtts import gTTS

if len(sys.argv) < 2:
    print 'Exiting ...'
    sys.exit(1)

with open(sys.argv[1], 'r') as fp:
    data = fp.read()
    tts = gTTS(data)
    tts.save('hello.mp3')
    
    
