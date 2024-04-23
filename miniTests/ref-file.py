# Echo can audibly respond to questions from the user.
# # Echo can audibly provide answers to question utilizing ONLY context from the call (ideal is considering protocol)
# # Echo can audibly resurface information from the collected radio transmissions

import os
import json
from playsound import playsound 
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

apiKey = os.getenv("APIKEY")
lang ='en'

client = OpenAI(api_key=apiKey)

# Text interface with chatgpt - this is what we'll change later when implementing speech recognition
def chatGPT(text):
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
                                    {"role": "system", "content": "You are a helpful assistant."},
                                    {"role": "user", "content": text}
                                 ]
                                 )
    chatText = completion.choices[0].message.content
    return chatText 

# Main function
def main():
    # Initial prompt
    print("Echo is ready to assist you. Please say something to get started.")
    
    # Main loop for continuously
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Exiting the program...")
            break

        # Call chatGPT function to get response
        response = chatGPT(user_input)
        
        # Print response
        print("Echo:", response)

if __name__ == "__main__":
    main()
