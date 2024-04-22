# Referencing the OpenAI API to transcribe audio files, testing how it works

from openai import OpenAI
client = OpenAI()

# Authorization: Bearer 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
  


audio_file= open("/path/to/file/audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whispper-1", 
  file=audio_file
)
print(transcription.text)