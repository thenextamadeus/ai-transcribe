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

response_1 = "Vitals Captured."
response_2 = "Echo to Unit 24, Receiving"
# response_3 = ""


# Sound files
soundEchoRunning = "../fresh-sounds/echo-running.wav"
soundEchoListening = "../fresh-sounds/echo-listening.wav"
soundEchoHeard = "../fresh-sounds/echo-heard.wav"
soundEchoIdle = "../fresh-sounds/echo-idle.wav"
soundEchoLeaving = "../fresh-sounds/echo-leaving.wav"


# Initialize a counter
counter = 1

def echoSpeaks(response):
    global counter

    # Increment the counter
    filename = f"./demo-audio/echo-says-{counter}.mp3"
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

    echoSpeaks(response_2)
    print("response_2: ", response_2)

    
    # echoSpeaks(response_3)
    # print("response_3: ", response_3)

# Run the main function
if __name__ == "__main__":
    main()  