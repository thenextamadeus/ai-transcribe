import json
from openai import OpenAI

# Load the JSON data
with open("ems_case_file.json", "r") as f:
    json_data = json.load(f)

# Update the JSON data based on the ChatGPT response
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Provide a brief summary for the EMS case file."}
    ]
)
chatText = completion.choices[0].message.content
json_data["ChiefComplaint"]["DispatchedPurpose"] = "Brief summary of the call purpose"
json_data["Assessment"]["AVPU"] = "Alert, Verbal, Painful, Unresponsive"
json_data["Assessment"]["Vitals"]["Pulse"] = 80
# Update other fields as needed

# Save the updated JSON data
with open("ems_case_file.json", "w") as f:
    json.dump(json_data, f, indent=4)

print("EMS case file updated.")