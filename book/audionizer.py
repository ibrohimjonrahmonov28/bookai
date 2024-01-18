from pathlib import Path
import openai

openai.api_key = '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'

speech_file_path = Path(__file__).parent / "speech.mp3"
response = openai.Completion.create(
    engine="tts-1",
    prompt="Today is a wonderful day to build something people love!",
)

response['choices'][0]['audio'].to_file(speech_file_path)
