import json

# Define the JSON file structure
json_data = {
    "ChiefComplaint": {
        "DispatchedPurpose": "",
        "SceneComponents": []
    },
    "History": {
        "PatientHistory": ""
    },
    "Assessment": {
        "AVPU": "",
        "OPQRST": "",
        "Vitals": {
            "Pulse": "0",
            "Respiration": "0",
            "BloodPressure": "",
            "Temperature": "0.0",
            "OxygenSaturation": "0"
        },
        "AudioRecording": ""
    },
    "Treatment": {
        "ProvidedTreatment": "",
        "AudioRecording": ""
    },
    "Transport": {
        "PatientStatus": "",
        "DropoffNotes": ""
    }
}

# Save the JSON data to a file
with open("./case-file/baseCase.json", "w") as f:
    json.dump(json_data, f, indent=4)

print("JSON file 'ems_case_file.json' created.")