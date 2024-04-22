from gtts import gTTS
from playsound import playsound 
# import os

file = open("abc.txt", "r").read().replace("\n", " ")
speech = gTTS(text = str(file),lang='en',slow = False)
speech.save("voice.mp3")
playsound("voice.mp3")