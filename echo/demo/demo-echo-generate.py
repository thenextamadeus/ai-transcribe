# Initialize libraries
import os
from playsound import playsound
from dotenv import load_dotenv
from openai import OpenAI

# Activate env
load_dotenv()
apiKey = os.getenv("APIKEY")
lang = 'en'
client = OpenAI(api_key=apiKey)

intent = "demo-echo.py is a demo day example of an extremely linear interaction with echo, WIZARD OF OZ PROTOTYPE"

response_1 = "Heart Rate Dropped Significantly. please recording vitals at 1 minute intervals."
FILENAME = "echo-says-suggestion.mp3"

# Initialize a counter
counter = 1

def echoSpeaks(response):
    global counter

    # Increment the counter
    filename = FILENAME
    counter += 1

    # Text to speech, using OpenAI
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=str(response)
    ) as response:
        # This doesn't seem to be *actually* streaming, it just creates the file
        # and then doesn't update it until the whole generation is finished
        response.stream_to_file(filename)

    playsound(filename)

def main():
    global counter

    echoSpeaks(response_1)
    print("response_1: ", response_1)

# Run the main function
if __name__ == "__main__":
    main()  