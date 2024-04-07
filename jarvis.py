# Based on Jarvis Video: https://www.youtube.com/watch?v=RAKpMYOlttA

import os
import time
import pyaudio
import speech_recognition as sr
from playsound import playsound 
from gtts import gTTS
from openai import OpenAI


apiKey = "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"
lang ='en'

client = OpenAI(api_key=apiKey)

guy = ""

while True:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            audio = r.listen(source, phrase_time_limit=20)
            print("source passed")
            said = ""

            try:
                print("initializing said")
                # Google Speech Recognition, Speech to text
                said = r.recognize_google(audio) # Google Speech Recognition

                # Attach the recognized speech to the global variable
                global guy 
                guy = said
                

                if "unit 24 to echo" in said:
                    print("call to action detected")

                    # Formatting the string
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print("request recorded: ", new_string) 

                    # Instruct ChatGPT, utilizing "said" 
                    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
                                                                    {"role": "system", "content": "You are a helpful assistant."},
                                                                    {"role": "user", "content": new_string}
                                                                 ]
                                                                 )
                    print("request passed to openai")
                    text = completion.choices[0].message
                    print("openAI response: ", text)
                    
                    text.read().replace("\n", " ")
                    print("formatting response: ", text)
                    # Text to speech, using gTTS
                    speech = gTTS(text = text, lang=lang, slow=False, tld="com.au")
                    print("text passed to gTTS")
                    speech.save("welcome1.mp3")
                    playsound.playsound("welcome1.mp3")
                    
            except Exception:
                print("Exception")


        return said

    if "stop" in guy:
        print("Stopping")
        break


    get_audio()