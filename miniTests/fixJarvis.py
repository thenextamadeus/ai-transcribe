# Debugging the microphone, and understanding how SR library works with GTT

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
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("source passed")
            said = ""

            try:
                print("Recognizing")
                said = r.recognize_google(audio)  # Google Speech Recognition
                print("You said:", said)

                # Check if "Friday" is in the recognized speech
                if "Friday" in said:
                    print("Friday detected")

                    # Uncomment the lines below to integrate with OpenAI and TTS
                    # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content":said}])
                    # text = completion.choices[0].message.content
                    # speech = gTTS(text = text, lang=lang, slow=False, tld="com.au")
                    # speech.save("welcome1.mp3")
                    # playsound.playsound("welcome1.mp3")
                    
            except Exception as e:
                print("Exception:", e)

        return said

    if "stop" in guy:
        print("Stopping")
        break

    audio_input = get_audio()
