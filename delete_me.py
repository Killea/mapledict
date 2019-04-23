
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


with open('D:/mapledict/temp/t.spx', 'rb') as f:
    data = f.read()
    print(data)

with open("D:/mapledict/temp/t.spx", "rb") as binary_file:
    # Read the whole file at once
    data = binary_file.read()
    print(data)

    