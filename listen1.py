import speech_recognition as sr

# Initialize SpeechRecognizer
recognizer = sr.Recognizer()

def test_microphone():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)  # Google Speech Recognition
        print("Speech recognized: " + text)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    test_microphone()
