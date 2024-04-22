# Initialize libraries

import os
import json
from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI
import speech_recognition as sr

# Activate env

load_dotenv()

apiKey = os.getenv("APIKEY")
lang ='en'

client = OpenAI(api_key=apiKey)


# Load JSON files
with open("./categories.json", "r") as f:
    categories = json.load(f)

with open("./youAreEcho.json", "r") as f:
    instructions = json.load(f)


# Load global variables

wordsSaid = ""


# Echo can transcribe and document information heard from the microphone
# # Echo is listening for trigger words relating to categories
# # Echo has categories like "vitals", "chief complaint", "scene info", "patient info", "patient history", "intervention", "time", "ems alert", "location"
# # Echo documents through text, the related information after each trigger word is detected
def listenForTriggers():
    yourVoice = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        audio = yourVoice.listen(source, phrase_time_limit=5)
        print("source passed")
        said = ""

        try:
            print("initializing said")
            # Google Speech Recognition, Speech to text
            said = yourVoice.recognize_google(audio) # Google Speech Recognition

            # Attach the recognized speech to the global variable
            global wordsSaid 
            wordsSaid = said

            if ("Echo" or "echo") in said:
                print("call to action detected")

                # Formatting the string
                words = said.split()
                new_string = ' '.join(words[1:])
                print("echo called", new_string) 

        


        except Exception:
                print("Sorry, I did not get that. Please repeat your request.")
        
        
        return said


def documentVoices():
    p = wordsSaid.split()

# Echo can scan multiple radio transmissions
# # Echo can transcribe radio transmissions
# # Echo provides a text summary of radio transmissions related to the call EMS is on
# # Echo can provide that summary audibaly to the user



# The user can communicate with Echo using the trigger word "Echo"
# # "Echo" is the beginning of a conversation between user and echo
# # Echo plays a sound when it is listening, and when complete



# Echo can audibly respond to questions from the user.
# # Echo can audibly provide answers to question utilizing ONLY context from the call (ideal is considering protocol)
# # Echo can audibly resurface information from the collected radio transmissions


# main function

def main():
    listenForTriggers()
    documentVoices()


if __name__ == "__main__":
    main()
