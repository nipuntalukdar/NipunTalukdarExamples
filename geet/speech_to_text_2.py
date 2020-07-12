import pyttsx3
import sys
from time import sleep
from random import randint
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 100)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[17].id)   #changing index, changes voices. 1 for female

def say_a_sentence(sentence, t):
    global engine
    print sentence
    engine.say(sentence)
    engine.runAndWait()
    if 'your address' in sentence:
        sleep(t * 3)
    else:
        sleep(t)

delay = 4
if len(sys.argv) >= 3:
    delay = float(sys.argv[2])

with open(sys.argv[1], 'r') as fp:
    alls = fp.readlines()
    lines = [l.strip() for l in alls]
    while True:
        say = lines[randint(0, len(lines) - 1)]
        say_a_sentence(say, delay)


engine.stop()

