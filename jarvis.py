import os
import time
import pyaudio
import speech_recognition as sr
from playsound import playsound 
from gtts import gTTS
import openai


api_key = "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"

lang ='en'

openai.api_key = api_key


guy = ""

while True:
    def get_adio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            audio = r.listen(source)
            print("source passed")
            said = ""

            try:
                print("Recognizing")
                said = r.recognize_google(audio) # Google Speech Recognition
                global guy 
                guy = said
                

                if "Friday" in said:
                    print("Friday")
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print(new_string) 
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content":said}])
                    text = completion.choices[0].message.content
                    speech = gTTS(text = text, lang=lang, slow=False, tld="com.au")
                    speech.save("welcome1.mp3")
                    playsound.playsound("welcome1.mp3")
                    
            except Exception:
                print("Exception")


        return said

    if "stop" in guy:
        print("Stopping")
        break


    get_adio()