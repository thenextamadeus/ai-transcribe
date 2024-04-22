import time
import speech_recognition as sr

def main():
    # Initialize the recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Adjust microphone for ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Calibrating microphone...")
        recognizer.pause_threshold = 1.0 

    # Main loop for continuously capturing and transcribing audio
    while True:
        # Capture audio from the microphone
        with microphone as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition with show_all=True
            print("Transcribing...")
            response = recognizer.recognize_google(audio, show_all=True)

            if response:
                # Get the most probable transcription
                text = response["alternative"][0]["transcript"]
                print("You said:", text)

                if "exit" in text:
                    print("Exiting the program...")
                    break

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service:", e)

        # Pause for a moment before capturing the next audio
        time.sleep(0.1)

if __name__ == "__main__":
    main()