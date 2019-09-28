'''
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')


engine.setProperty('voice', voices[1].id)
engine.say("a humorous way of telling someone to shut the door after they come into a room or building")
engine.runAndWait()
engine.stop()
'''

'''
from kivy.core.audio import SoundLoader

sound = SoundLoader.load('D:/mapledict/temp/t.spx')
if sound:
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()
    '''

'''
import vlc

player = vlc.MediaPlayer("D:/mapledict/temp/t.spx")
player.play()
'''

'''
import json

with open ('z.json','rb') as text:
    json_file = text.read()
    dict1 = json.loads(json_file)

    print(dict1)
'''

'''
import time
start = time.time()
from pattern.en import lemma


print(lemma('foods'))

#long running
#do something other
end = time.time()
print (end-start)
'''

import spell

print(spell.correction('speling'))