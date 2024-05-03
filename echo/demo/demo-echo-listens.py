import time
from playsound import playsound
from pynput import keyboard
import speech_recognition as sr

# Define global variables for audio file paths
AUDIO_FILE_PATH_PRESS = "./demo-audio/echo-listening.wav"
AUDIO_FILE_PATH_RELEASE = "./demo-audio/echo-heard.wav"
AUDIO_FILE_PATH_NOTIFY = "./demo-audio/echo-notify.wav"
AUDIO_FILE_PATH_ACKNOWLEDGE = "./demo-audio/echo-says-1.mp3"
AUDIO_FILE_PATH_SUMMARY = "./demo-audio/echo-says-takeVitals.mp3"

# Global Parameters for Speech Recognition
mic = sr.Microphone(0)
r = sr.Recognizer()
gPause = 0.7 # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
gPhrase = 3 # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.

# Trigger Detection Parameters (shorter = potential faster response)
tPause = 0.5
tPhrase = 3  

# Boolean variable to track if spacebar is currently pressed
spacebar_pressed = False


# Function to recognize speech
def recognizeSpeech():
    r.pause_threshold = gPause
    r.phrase_threshold = gPhrase

    with mic as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=gPhrase)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")  
        except sr.UnknownValueError:
            print("...")
        except sr.RequestError as e:
            print(f"error; {e}")


# Function to handle key press event
def on_press(key):
    global spacebar_pressed
    if key == keyboard.Key.space and not spacebar_pressed:
        print('Spacebar pressed')
        playsound(AUDIO_FILE_PATH_PRESS)
        # recognizeSpeech()
        spacebar_pressed = True

# Function to handle key release event
def on_release(key):
    global spacebar_pressed
    if key == keyboard.Key.space:
        print('Spacebar released')
        playsound(AUDIO_FILE_PATH_RELEASE)
        playsound(AUDIO_FILE_PATH_ACKNOWLEDGE)
        time.sleep(1)
        playsound(AUDIO_FILE_PATH_NOTIFY)
        playsound(AUDIO_FILE_PATH_SUMMARY)
    elif key == keyboard.Key.esc:
        print('Exiting the program...')
        return False  # Stop listener to exit the program

# Start listener to detect key press and release events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Main loop: Keep the program running
while True:
    # Do nothing, just keep the program running
    time.sleep(1)

    # When false is returned from on_release, exit the program
    if not listener.running:
        break