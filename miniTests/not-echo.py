import os
import json
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
source = sr.Microphone()
r = sr.Recognizer()
gPause = 0.7
gPhrase = 3

# Trigger Detection Parameters (shorter = potential faster response)
tPause = 0.5
tPhrase = 3



# Load JSON files
vitals_data = {}

vitals_file = "./instructions/document.json"

# Load existing data if the file exists
if os.path.exists(vitals_file):
    with open(vitals_file, "r") as f:
        vitals_data = json.load(f)

with open(vitals_file, "r") as f:
    categories = json.load(f)

with open("instructions/youAreEcho.json", "r") as f:
    instructions = json.load(f)

# Load global variables
folder_path = "./radioTranscribe"

wordsSaid = ""

# Define states
STATE_IDLE = 0
STATE_LISTENING = 1
STATE_ACTIVE = 2

# Initialize state
state = STATE_IDLE

# Functions for handling different states

def handle_idle_state(audio, pause_threshold, phrase_time_limit):
    try:
        r.pause_threshold = pause_threshold
        r.phrase_time_limit = phrase_time_limit
        text = r.recognize_google(audio).lower()
        if "echo" in text:
            print("Entering listening state...")
            playsound("../sounds/echo-on.wav")  # Play sound to indicate listening
            return STATE_LISTENING
        elif "exit exit" in text:
            print("Exiting the program...")
            return None
    except sr.UnknownValueError:
        print("...")

    return STATE_IDLE

def handle_listening_state(audio, pause_threshold, phrase_time_limit):
    try:
        
        text = r.recognize_google(audio).lower()
        if "document" in text:
            document(pause_threshold, phrase_time_limit)
            return STATE_ACTIVE
        elif "no further" in text:
            print("Returning to idle state...")
            return STATE_IDLE
    except sr.UnknownValueError:
        print("...")

    return STATE_LISTENING

def handle_active_state(audio, pause_threshold, phrase_time_limit):
    try:
        r.pause_threshold = pause_threshold
        r.phrase_time_limit = phrase_time_limit
        text = r.recognize_google(audio).lower()
        if "no further" in text:
            print("Returning to idle state...")
            return STATE_IDLE
    except sr.UnknownValueError:
        print("...")

    return STATE_ACTIVE

# Function to document vitals
def document(pause_threshold, phrase_time_limit):
    global vitals_data
    
    with sr.Microphone() as source:
        r.pause_threshold = pause_threshold
        r.phrase_time_limit = phrase_time_limit

        print("Listening for vitals...")
        audio = r.listen(source, phrase_time_limit=phrase_time_limit)

        try:
            vitals_text = r.recognize_google(audio)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vitals_data[f"vitals_recording-{timestamp}"] = vitals_text
            print("Vitals recorded.")

            # Call chatGPT function to get response
            initial_prompt = f"{instructions['objective']}\n{instructions['context']}\n{instructions['audience']}\n{instructions['tone']}\n\nVitals Data:\n{json.dumps(vitals_data, indent=2)}"
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": vitals_text}
                ]
            )
            chatText = completion.choices[0].message.content
            print("Echo: ", chatText)

            echoSpeaks(chatText)

        except sr.UnknownValueError:
            print("...")

    save_vitals_data()

def echoSpeaks(response):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=str(response)
    ) as response:
        response.stream_to_file("../sounds/echo-v2-talks.mp3")

    playsound("../sounds/echo-v2-talks.mp3")

def save_vitals_data():
    with open("vitals_data.json", "w") as f:
        json.dump(vitals_data, f, indent=4)

# Main loop
while state is not None:
    print("Echo Listening...")
    audio = r.listen(source, phrase_time_limit=gPhrase)
    
    if state == STATE_IDLE:
        state = handle_idle_state(audio, tPause, tPhrase)
    elif state == STATE_LISTENING:
        state = handle_listening_state(audio, gPause, gPhrase)
    elif state == STATE_ACTIVE:
        state = handle_active_state(audio, gPause, gPhrase)
