from pynput import keyboard
import time
from playsound import playsound

# Define the key to detect
key_to_detect = keyboard.Key.space

# Function to play audio when key is pressed
def play_audio_pressed():
    playsound("../fresh-sounds/echo-listening.wav")

# Function to play audio when key is released
def play_audio_released():
    playsound("../fresh-sounds/echo-heard.wav")

# Function to handle key press event
def on_key_press(key):
    if key == key_to_detect:
        print("Key pressed")
        play_audio_pressed()

# Function to handle key release event
def on_key_release(key):
    if key == key_to_detect:
        print("Key released")
        play_audio_released()

# Start listener
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()
