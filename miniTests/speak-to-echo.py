# Echo can audibly respond to questions from the user.
# # Echo can audibly provide answers to question utilizing ONLY context from the call (ideal is considering protocol)
# # Echo can audibly resurface information from the collected radio transmissions

import os
import json
from playsound import playsound 
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import speech_recognition as sr
import json
from gtts import gTTS
from datetime import datetime



load_dotenv()

apiKey = os.getenv("APIKEY")
lang ='en'

client = OpenAI(api_key=apiKey)

intent = "speak-to-echo.py is a test to understand how sr triggers translates to a conversation between AI and user."


# Echo can transcribe and document information heard from the microphone


# Global Parameters for Speech Recognition
r = sr.Recognizer()
r.pause_threshold = 2  # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
r.phrase_time_limit = 8  # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.


# # # # # Echo Actions # # # #
def echo():

    # Trigger Detection Parameters (shorter = potential faster response)
    r.pause_threshold = 0.7
    r.phrase_time_limit = 3

    with sr.Microphone() as source:
        # play sound to indicate listening
        playsound("../sounds/echo-on.wav")

        print("Listening...")
        audio = r.listen(source)
        

        try:
            user_text = r.recognize_google(audio)
            print("Echo Heard: ", user_text)
            # play sound to indicate heard
            playsound("../sounds/echo-heard.wav")

        except sr.UnknownValueError:
            print("...")
            playsound("../sounds/echo-error.wav")
            return

        # Call chatGPT function to get response
        # response = chatGPT(user_input)
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You are simply answering questions as well as you can. Be funny, dramatic, and silly"},
            {"role": "user", "content": user_text}
            ]
            )

        chatText = completion.choices[0].message.content
        print("Echo: ", chatText)

        echoSpeaks(chatText)


def echoSpeaks(response):
    # # Text to speech, using gTTS ----------------------------------------------------------------------------
    # speech = gTTS(text = str(response), lang=lang, slow=False, tld="com.au")
    # print("text passed to gTTS")
    # speech.save("../sounds/echo-v1-talks.mp3")
    
    # playsound("../sounds/echo-v1-talks.mp3")


    # Text to speech, using OpenAI --------------------------------------------------------------------------
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=str(response)
    ) as response:
        # This doesn't seem to be *actually* streaming, it just creates the file
        # and then doesn't update it until the whole generation is finished
        response.stream_to_file("../sounds/echo-v2-talks.mp3")

    playsound("../sounds/echo-v2-talks.mp3")

# # # # Trigger Actions # # # #
trigger_actions = {
    "echo": echo,
}



# Main loop for continuously capturing, triggering actions, and transcribing audio
with sr.Microphone() as source:
    print(intent)
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=5)
    print("Microphone calibrated.")
    
    # Trigger Detection Parameters (shorter = potential faster response)
    r.pause_threshold = 0.5
    r.phrase_time_limit = 3

    while True:
        print("Echo Listening...")
        audio = r.listen(source, phrase_time_limit=r.phrase_time_limit)

        try:
            response = r.recognize_google(audio, show_all=True)
            if response:
                text = response["alternative"][0]["transcript"].lower()
                print("Echo Heard: ", text)

                for trigger, action in trigger_actions.items():
                    if trigger in text:
                        action()
                        break
                
                if "exit exit" in text:
                    print("Exiting the program...")
                    break

        except sr.UnknownValueError:
            print("...")