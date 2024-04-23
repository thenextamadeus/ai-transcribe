# Echo can transcribe and document information heard from the microphone

import speech_recognition as sr
intent = "sr-params.py tests Google's Speech Recognition parameters for microphone tests."

r = sr.Recognizer()
r.pause_threshold = 0.7  # This represents the minimum length of silence (in seconds) that will register as the end of a phrase. The recognizer keeps listening until it encounters this duration of silence after speech.
r.phrase_time_limit = 8  # This is the maximum number of seconds that the recognizer will allow a phrase to continue before stopping and returning the audio captured until that point.


with sr.Microphone() as source:
    print(intent)
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=5)
    print("Microphone calibrated.")

# Main loop for continuously capturing and transcribing audio
    while True:
        print("Say something...")
        audio = r.listen(source, phrase_time_limit=r.phrase_time_limit)
        # Transcribe audio data)
        try: # Recognize speech using Google Speech Recognition with show_all=True
            print("Transcribing...")
            response = r.recognize_google(audio, show_all=True)

            if response:
                # Get the most probable transcription
                text = response["alternative"][0]["transcript"]
                print("You said:", text)

            if "exit" in text:
                print("Exiting the program...")
                break

        except sr.UnknownValueError:
            print("...")