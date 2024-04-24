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

intent = "ref-file.py is a test to orient ChatGPT responses based off of JSON files."

# Text interface with chatgpt - this is what we'll change later when implementing speech recognition
def chatGPT(text):
    # Load situation context from JSON file
    with open("situation_context.json", "r") as f:
        situation_context = json.load(f)

    # Load vitals data from JSON file
    with open("vitals_data.json", "r") as f:
        vitals_data = json.load(f)

    
    # Construct the initial prompt with situation context and vitals data
    initial_prompt = f"{situation_context['role']}\n{situation_context['situation']}\n{situation_context['guidelines']}\n\nVitals Data:\n{json.dumps(vitals_data, indent=2)}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": text}
        ]
    )

    chatText = completion.choices[0].message.content
    return chatText

# Main function
def main():
    # Initial prompt
    print(intent)
    print("Echo is ready to assist you.")
    
    # Main loop for continuously
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == "exit exit":
            print("Exiting the program...")
            break

        # Call chatGPT function to get response
        response = chatGPT(user_input)
        
        # Print response
        print("Echo:", response)

if __name__ == "__main__":
    main()
