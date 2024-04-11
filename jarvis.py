# Based on Jarvis Video: https://www.youtube.com/watch?v=RAKpMYOlttA
# GTT for Recognition https://stackoverflow.com/questions/59272258/how-to-use-gtts-library-to-read-a-text-file
# And utilizing ChatGPT
# And Whisper STT https://platform.openai.com/docs/guides/text-to-speech
# # Formerly GTT for STT https://stackoverflow.com/questions/59272258/how-to-use-gtts-library-to-read-a-text-file
# and playsound for audio https://pypi.org/project/playsound/

import os
import time
import pyaudio
from dotenv import load_dotenv
import speech_recognition as sr
from playsound import playsound 
from gtts import gTTS
from openai import OpenAI

load_dotenv()

apiKey = os.getenv("APIKEY")
lang ='en'

client = OpenAI(api_key=apiKey)

guy = ""

while True:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            audio = r.listen(source, phrase_time_limit=5)
            print("source passed")
            said = ""

            try:
                print("initializing said")
                # Google Speech Recognition, Speech to text
                said = r.recognize_google(audio) # Google Speech Recognition

                # Attach the recognized speech to the global variable
                global guy 
                guy = said
                

                if ("Echo" or "echo") in said:
                    print("call to action detected")

                    # Formatting the string
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print("request recorded: ", new_string) 

                    # Instruct ChatGPT, utilizing "said" 
                    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
                                                                    {"role": "system", "content": "You are a helpful assistant."},
                                                                    {"role": "user", "content": new_string}
                                                                 ]
                                                                 )
                    print("request passed to openai")
                    chatText = completion.choices[0].message.content
                    print("openAI response: ", chatText)
                    

                    # # Text to speech, using gTTS ----------------------------------------------------------------------------
                    # speech = gTTS(text = str(chatText), lang=lang, slow=False, tld="com.au")
                    # print("text passed to gTTS")
                    # speech.save("welcome1.mp3")
                    # playsound("welcome1.mp3")


                    # # Text to speech, using OpenAI --------------------------------------------------------------------------
                    # with client.audio.speech.with_streaming_response.create(
                    #     model="tts-1",
                    #     voice="nova",
                    #     input=str(chatText)
                    # ) as response:
                    # # This doesn't seem to be *actually* streaming, it just creates the file
                    # # and then doesn't update it until the whole generation is finished
                    #     response.stream_to_file("ttsResponses/speech.mp3")

                    # playsound("ttsResponses/speech.mp3")

                    
            except Exception:
                print("Exception")


        return said

    if "stop" in guy:
        print("Stopping")
        break


    get_audio()