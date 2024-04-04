import whisper

# Initialize Whisper.ai Speech Recognizer
whisper_client = whisper.Client()

def test_whisper_connection():
    with whisper.Microphone() as source:
        print("Listening...")
        audio = whisper_client.listen(source)

    try:
        text = whisper_client.recognize(audio)  # Whisper.ai Speech Recognition
        print("Whisper.ai recognized: " + text)
    except whisper.UnknownValueError:
        print("Whisper.ai could not understand audio")
    except whisper.RequestError as e:
        print("Could not request results from Whisper.ai service; {0}".format(e))

if __name__ == "__main__":
    test_whisper_connection()
