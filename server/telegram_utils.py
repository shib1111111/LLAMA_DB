import requests
from fastapi import FastAPI, Request, Response
from config import TELEGRAM_SECRET_KEY,GROQ_API_KEY
from groq import Groq

telegram_token = TELEGRAM_SECRET_KEY
telegram_client = Groq(api_key=GROQ_API_KEY)

# To Get Chat ID and message which is sent by client
def message_parser(message):
    try:
        chat_id = message['message']['chat']['id']
        if 'text' in message['message']:
            text = message['message']['text']
            print("Chat ID: ", chat_id)
            print("Message: ", text)
            return chat_id, text
        elif 'voice' in message['message']:
            file_id = message['message']['voice']['file_id']
            print("Chat ID: ", chat_id)
            print("Voice Message File ID: ", file_id)
            text = voice_to_text(file_id)
            return chat_id, text
        else:
            print("Unknown message type")
            return chat_id, "Unknown message type"
    except KeyError as e:
        print(f"Error parsing message: {e}")
        return None, None
        
def get_voice_file_url(file_id):
    try:
        url = f'https://api.telegram.org/bot{telegram_token}/getFile?file_id={file_id}'
        response = requests.get(url)
        response.raise_for_status()
        file_path = response.json()['result']['file_path']
        file_url = f'https://api.telegram.org/file/bot{telegram_token}/{file_path}'
        return file_url
    except requests.exceptions.RequestException as e:
        print(f"Error getting file URL: {e}")
        return None

def voice_to_text(file_id):
    file_url = get_voice_file_url(file_id)
    if not file_url:
        return "Unable to get voice file URL."

    try:
        # Download the voice file
        response = requests.get(file_url)
        response.raise_for_status()
        audio_data = response.content

        # Use Groq API to transcribe the audio
        transcription = telegram_client.audio.transcriptions.create(
            file=(f"voice_message_{file_id}.ogg", audio_data),
            model="whisper-large-v3",
            prompt="Specify transcription",
            response_format="json",
            language="en",
            temperature=0.0
        )
        return transcription.text
    
    except requests.exceptions.RequestException as e:
        return f"Unable to transcribe voice message."
    
    except Exception as e:
        return f"Unable to transcribe voice message."
# To send message using "SendMessage" API
def send_message_telegram(chat_id, text):
    try:
        url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None
