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
lang ='en'

client = OpenAI(api_key=apiKey)

intent = "echo.py is a mega-file that references JSON files to respond to EMS questions."


# Global Parameters for Speech Recognition
r = sr.Recognizer()
gPause = 0.7 # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
gPhrase = 3 # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.

# Trigger Detection Parameters (shorter = potential faster response)
tPause = 0.5
tPhrase = 3

# Load JSON files
vitals_data = {}

vitals_file = Path("./instructions/document.json")

# Load existing data if the file exists
if vitals_file.exists():
    with open(vitals_file, "r") as f:
        vitals_data = json.load(f)

with open("./instructions/document.json", "r") as f:
    categories = json.load(f)

with open("instructions/youAreEcho.json", "r") as f:
    instructions = json.load(f)

# Load global variables
folder_path = "./radioTranscribe"

wordsSaid = ""


# Echo can transcribe and document information heard from the microphone
# # Echo is listening for trigger words relating to categories
# # Echo has categories like "vitals", "chief complaint", "scene info", "patient info", "patient history", "intervention", "time", "ems alert", "location"
# # Echo documents through text, the related information after each trigger word is detected

# VITALS TRACKING # VITALS TRACKING # VITALS TRACKING # VITALS TRACKING
def document():
    print("document()")

    with sr.Microphone() as source:
        r.pause_threshold = gPause  # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
        r.phrase_time_limit = gPhrase # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.

        print("Listening for vitals...")
        audio = r.listen(source, phrase_time_limit=r.phrase_time_limit)

        try:
            vitals_text = r.recognize_google(audio)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vitals_data[f"vitals_recording-{timestamp}"] = vitals_text
            print("Vitals recorded.")

        except sr.UnknownValueError:
            print("...")

    save_vitals_data()

def save_vitals_data():
    with open("vitals_data.json", "w") as f:
        json.dump(vitals_data, f, indent=4)



# Echo can scan multiple radio transmissions
# # Echo can transcribe radio transmissions
# # Echo provides a text summary of radio transmissions related to the call EMS is on
# # Echo can provide that summary audibaly to the user
def transcribe(folder_path, batch_size=10, output_file='transcriptions.json'):
    context = {"Context": "The following is a transcript from an incoming dispatch call"}

    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            transcriptions = json.load(f)
    else:
        transcriptions = {}

    files = [f for f in os.listdir(folder_path) if f.endswith(".wav")]
    total_files = len(files)
    processed_files = 0

    while processed_files < total_files:
        batch_files = files[processed_files:processed_files + batch_size]
        for filename in batch_files:
            print(f"Processing {filename}...")
            audio_file = os.path.join(folder_path, filename)
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                print(f"Recognizing {filename}...")
                audio_data = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_data)
                transcriptions[filename] = transcription
            except sr.UnknownValueError:
                print(f"Couldn't Determine {filename}")
            except sr.RequestError as e:
                print(f"Error; {e}")

        with open(output_file, 'w') as f:
            output_data = {**context, **transcriptions}
            json.dump(output_data, f, indent=4)

        processed_files += batch_size

    return transcriptions

def summaryIncoming():
    print("Nothing to transcribe yet.")



# The user can communicate with Echo using the trigger word "Echo"
# # "Echo" is the beginning of a conversation between user and echo
# # Echo plays a sound when it is listening, and when complete
def echo():

    
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
        # Construct the initial prompt with situation context and vitals data
        initial_prompt = f"{instructions['objective']}\n{instructions['context']}\n{instructions['audience']}\n{instructions['tone']}\n\nVitals Data:\n{json.dumps(vitals_data, indent=2)}"

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": user_text}
            ]
        )

        chatText = completion.choices[0].message.content
        print("Echo: ", chatText)

        echoSpeaks(chatText)



# Echo can audibly respond to questions from the user.
# # Echo can audibly provide answers to question utilizing ONLY context from the call (ideal is considering protocol)
# # Echo can audibly resurface information from the collected radio transmissions
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
    "document": document,
}


# main function
with sr.Microphone() as source:
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

