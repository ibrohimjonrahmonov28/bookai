# from pathlib import Path
# from openai import OpenAI
# client = OpenAI(api_key="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")
# def audionizer(text):
#   speech_file_path = Path(__file__).parent / "speech.mp3"
#   response = client.audio.speech.create(
#     model="tts-1",
#     voice="alloy",
#     input=""
#   )

#   response.stream_to_file(speech_file_path)


from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key="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")

def audionizer(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text  # Pass the input text here
    )

    # Ensure the response is successful before attempting to save the file
    # if response.status_code == 200:
        # Save the audio file
    with open(speech_file_path, 'wb') as f:
            f.write(response.content)
    # else:
        # print(f"Error: {response.status_code} - {response.text}")
