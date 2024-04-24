import os
import json
from gtts import gTTS
import speech_recognition as sr


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


def main():
    folder_path = "./radioTranscribe"
    transcribe(folder_path)


if __name__ == "__main__":
    main()