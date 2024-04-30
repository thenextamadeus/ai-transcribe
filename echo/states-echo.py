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

intent = "states-echo.py is a file that organizes echo functions into an intuitive interactive VUI."


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

# Define states
STATE_IDLE = 0
STATE_LISTENING = 1
STATE_ACTIVE = 2
STATE_EXIT = 3


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

    


# Main Functions
def echo(text):
    print("Echo function called.")
    # Call chatGPT function to get response
    # response = chatGPT(user_input)
    # Construct the initial prompt with situation context and vitals data
    initial_prompt = f"{instructions['objective']}\n{instructions['context']}\n{instructions['audience']}\n{instructions['tone']}\n\nVitals Data:\n{json.dumps(vitals_data, indent=2)}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": text}
        ]
    )

    chatText = completion.choices[0].message.content
    print("Echo: ", chatText)

    echoSpeaks(chatText)


def echoSpeaks(response):
    # Text to speech, using gTTS ----------------------------------------------------------------------------
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
        response.stream_to_file("../sounds/echo-v3-talks.mp3")

    playsound("../sounds/echo-v3-talks.mp3")


# VITALS TRACKING # VITALS TRACKING # VITALS TRACKING # VITALS TRACKING
def document(text):
    print("document()")
    # vitals_text = r.recognize_google(text)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vitals_data[f"vitals_recording-{timestamp}"] = text
    print("Vitals recorded.")

    save_vitals_data()

def save_vitals_data():
    with open(vitals_file, "w") as f:
        json.dump(vitals_data, f, indent=4)



# Trigger Actions
trigger_actions = {
    "document": document,
}



# Function to handle state transitions and trigger actions
def handle_interaction(audio, state):
    try:
        response = r.recognize_google(audio, show_all=True)
        if response:
            text = response["alternative"][0]["transcript"].lower()
            print("Echo Heard: ", text)

            if state == STATE_IDLE:
                if "echo" in text:
                    print("Entering listening state...")
                    playsound(soundEchoListening)  # Play sound to indicate listening
                    return STATE_LISTENING
                
                if "terminate" in text:
                    return STATE_EXIT

            elif state == STATE_LISTENING:
                for trigger, action in trigger_actions.items():
                    if trigger in text:
                        action(text)
                        playsound(soundEchoHeard)  # Play sound to indicate heard
                        print("Entering active state...")
                        return STATE_ACTIVE
                
                if "no further" in text:
                    print("Returning to idle state...")
                    playsound(soundEchoIdle)
                    return STATE_IDLE
                
                
                else:
                    playsound(soundEchoHeard)  # Play sound to indicate heard
                    echo(text)
                    return STATE_ACTIVE
                

            elif state == STATE_ACTIVE:
                for trigger, action in trigger_actions.items():
                    if trigger in text:
                        action(text)
                        playsound(soundEchoHeard)  # Play sound to indicate heard
                
                if "no further" in text:
                    print("Returning to idle state...")
                    playsound(soundEchoIdle)
                    return STATE_IDLE
                
                else:
                    playsound(soundEchoHeard)  # Play sound to indicate heard
                    echo(text)

                

    except sr.UnknownValueError:
        print("...")

    return state  # No state change


# Main function
with mic as source:
    print("Calibrating audio...")
    r.adjust_for_ambient_noise(source)
    print("Calibration complete.")
    playsound(soundEchoRunning)

    # Trigger Detection Parameters (shorter = potential faster response)
    r.pause_threshold = tPause
    r.phrase_time_limit = tPhrase

    state = STATE_IDLE

    while True:
        print("Echo Listening...")
        audio = r.listen(source, phrase_time_limit=r.phrase_time_limit)

        state = handle_interaction(audio, state)

        if state == STATE_EXIT:
            print("Exiting the program...")
            playsound(soundEchoLeaving)
            break
