# Echo can transcribe and document information heard from the microphone


from pathlib import Path
import speech_recognition as sr
import json
from datetime import datetime

intent = "sr-triggers.py listens for trigger words and documets actions that transcribe audio following the trigger word."

# Global Parameters for Speech Recognition
r = sr.Recognizer()
r.pause_threshold = 0.7  # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
r.phrase_time_limit = 8  # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.


# # # # Echo Actions # # # # 

# VITALS TRACKING

vitals_data = {}

vitals_file = Path("vitals_data.json")

# Load existing data if the file exists
if vitals_file.exists():
    with open(vitals_file, "r") as f:
        vitals_data = json.load(f)



def document_vitals():
    print("document_vitals()")

    with sr.Microphone() as source:
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




# # # # Trigger Actions # # # #
trigger_actions = {
    "document vitals": document_vitals,
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
                
                if "exit" in text:
                    print("Exiting the program...")
                    break

        except sr.UnknownValueError:
            print("...")