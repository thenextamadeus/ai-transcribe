# Initialize libraries
import os
import json
from pathlib import Path
from datetime import datetime
from playsound import playsound
from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI
import speech_recognition as sr

# Activate env
load_dotenv()
apiKey = os.getenv("APIKEY")
lang = 'en'
client = OpenAI(api_key=apiKey)

intent = "demo-echo.py is a demo day example of an extremely linear interaction with echo, based off a script."


# Define global variables
# Define speech recognition variables
mic = sr.Microphone()
r = sr.Recognizer()


# Sound files
soundEchoRunning = "../fresh-sounds/echo-running.wav"
soundEchoListening = "../fresh-sounds/echo-listening.wav"
soundEchoHeard = "../fresh-sounds/echo-heard.wav"
soundEchoIdle = "../fresh-sounds/echo-idle.wav"
soundEchoLeaving = "../fresh-sounds/echo-leaving.wav"

# Global phrase/pause parameters
gPause = 0.7  # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
gPhrase = 5  # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.

# Trigger detection parameters (shorter = potential faster response)
tPause = 1
tPhrase = 5


# Load JSON files
vitals_data = {}

# Instruction Files
vitals_file = Path("./instructions/document.json")

# Load existing data if the file exists
if vitals_file.exists():
    with open(vitals_file, "r") as f:
        vitals_data = json.load(f)

with open("./instructions/youAreEcho.json", "r") as f:
    instructions = json.load(f)


with open(vitals_file, "r") as f:
    categories = json.load(f)

# The Script
# Note that this would be possible with echo, but for the simplicity of the audience, we will be using a linear script
# # Hey Echo
# # Echo Beeps
# # Document Vitals
# # Echo Vitals Captured OR Beep
# # be able to be silently listening for document again
# # Document Vitals 2.0
# # Call echo to notify us of the idfference
# # Thanks echo
# # Echo Beeps



# main function
with mic as source:
    print(intent)
    # print("Transcribing incoming dispatch calls")
    # transcribe(folder_path)

    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=5)
    print("Microphone calibrated.")

    # summaryIncoming()
    

    # Trigger Detection Parameters (shorter = potential faster response)
    r.pause_threshold = tPause
    r.phrase_time_limit = tPhrase

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

