# Bug fix from OpenAI documentation, github comment https://github.com/openai/openai-python/issues/864#issuecomment-1962128107

from openai import OpenAI

apiKey = "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"
client = OpenAI(api_key=apiKey)

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="""I see skies of blue and clouds of white
             The bright blessed days, the dark sacred nights
             And I think to myself
             What a wonderful world""",
) as response:
    # This doesn't seem to be *actually* streaming, it just creates the file
    # and then doesn't update it until the whole generation is finished
    response.stream_to_file("ttsResponses/speech.mp3")