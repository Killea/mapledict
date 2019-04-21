import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')


engine.setProperty('voice', voices[1].id)
engine.say("a humorous way of telling someone to shut the door after they come into a room or building")
engine.runAndWait()
engine.stop()