from config import GROQ_API_KEY
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_data):
    try:
        transcription = client.audio.transcriptions.create(
            file=(f"voice_message.ogg", audio_data),
            model="whisper-large-v3",
            prompt="Specify transcription",
            response_format="json",
            language="en",
            temperature=0.0
        )
        return transcription.text
    except Exception as e:
        return f"Unable to transcribe voice message."