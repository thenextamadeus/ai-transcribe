import os
import json
from gtts import gTTS
from openai import OpenAI
import speech_recognition as sr

# Initialize OpenAI client
apiKey = os.getenv("APIKEY")
client = OpenAI(api_key=apiKey)

# Define categories
categories = ["TIME", "EMS ALERT", "LOCATION", "SCENE INFO", "CHIEF COMPLAINT", "PATIENT INFO", "PATIENT HISTORY", "INTERVENTION"]


# # # THIS IS TRANSCIBING AND CREATING CASE FILE

# Function to transcribe audio files using Google's Speech Recognition
def transcribe(folder_path):
    transcriptions = {}
    for filename in os.listdir(folder_path):
        print(f"Processing {filename}...")
        if filename.endswith(".wav"):  # Assuming audio files are in m4a format
            # Load the audio file
            audio_file = os.path.join(folder_path, filename)
            # Initialize the recognizer
            recognizer = sr.Recognizer()
            # Load the audio file
            with sr.AudioFile(audio_file) as source:
                print(f"Recognizing {filename}...")
                audio_data = recognizer.record(source)
                # Use Google's Speech Recognition to transcribe the audio
                try:
                    transcription = recognizer.recognize_google(audio_data)
                    transcriptions[filename] = transcription
                except sr.UnknownValueError:
                    print(f"Google Speech Recognition could not understand audio in {filename}")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
    return transcriptions


# Function to categorize transcriptions
def categorize(transcriptions):
    categorized_data = {}
    for filename, transcription in transcriptions.items():
        # Construct the input message for ChatGPT
        messages = [
            {"role": "system", "content": "You are a virtual assistant designed to categorize transcriptions of radio transmissions."},
            {"role": "system", "content": "Your goal is to categorize the transcriptions into predefined categories."},
            {"role": "system", "content": "The categories include: 'TIME', 'EMS ALERT', 'LOCATION', 'SCENE INFO', 'CHIEF COMPLAINT', 'PATIENT INFO', 'PATIENT HISTORY', and 'INTERVENTION'."},
            {"role": "system", "content": "Your responses should provide information relevant to these categories."},
            {"role": "system", "content": "You can use the context provided in the transcriptions and any additional information needed to categorize effectively."},
            {"role": "system", "content": "Ensure that the output is concise, accurate, and aligned with the content of the transcriptions."},
            {"role": "system", "content": "Please generate categorized responses based on the input transcriptions."},
            {"role": "user", "content": transcription}
        ]
        # Instruct ChatGPT with the messages
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        # Extract the categorized transcription from the response
        categorized_transcription = completion.choices[0].message.content
        # Store the categorized transcription
        categorized_data[filename] = categorized_transcription
    return categorized_data


# Function to generate JSON with focused information
def generate_json(categorized_data):
    # Save the categorized data directly to a JSON file
    with open("output.json", "w") as json_file:
        json.dump(categorized_data, json_file, indent=4)



# # # THIS IS THE RESPONSE PART

# Function to load JSON file
def load_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            categorized_data = json.load(json_file)
        return categorized_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file: {e}")
        return {}


# Function to interact with ChatGPT
def chat_with_gpt(user_input, categorized_data):
    # Construct initial message with all category information
    messages = [{"role": "system", "content": category_info} for category_info in categorized_data.values()]
    # Append user input to messages
    messages.append({"role": "user", "content": user_input})
    # Send messages to ChatGPT
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    # Get response from ChatGPT
    response = completion.choices[0].message.content
    return response


# Function to handle user interactions
def chat_interaction(initial_context):
    # Load the JSON file containing categorized data
    categorized_data = load_json(initial_context)
    
    # Start the interaction loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the loop if user input is "exit"
        if user_input.lower() == "exit":
            print("Exiting chat.")
            break
        
        # Pass user input to ChatGPT and get response
        response = chat_with_gpt(user_input, categorized_data)
        
        # Print ChatGPT's response
        print("ChatGPT:", response)


# Running the program
def main():
    # Define folder path containing audio files
    folder_path = "./radioComms/wav"
    print("Locating audio files...")
    
    # Transcribe audio files
    transcriptions = transcribe(folder_path)
    print("Transcriptions completed.")
    print(transcriptions)
    
    # Categorize transcriptions
    categorized_data = categorize(transcriptions)
    print("Categorization completed.")
    
    # Generate JSON with focused information
    generate_json(categorized_data)
    print("JSON file created with focused information.")
    
    # Define initial context (JSON file path)
    initial_context = "output.json"

    # Start the chat interaction
    chat_interaction(initial_context)


if __name__ == "__main__":
    main()
