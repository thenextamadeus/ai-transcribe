import speech_recognition as sr

r = sr.Recognizer()
r.pause_threshold = 0.7  # Adjust based on your scenario
r.phrase_time_limit = 8  # Adjust as needed

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source, phrase_time_limit=r.phrase_time_limit)

    # Transcribe audio data
