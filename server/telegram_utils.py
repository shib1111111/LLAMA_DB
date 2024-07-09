import requests
from fastapi import FastAPI, Request, Response
from config import TELEGRAM_SECRET_KEY

telegram_token = TELEGRAM_SECRET_KEY

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
            break
            text = voice_to_text(file_id)
            return chat_id, text
        else:
            print("Unknown message type")
            return chat_id, "Unknown message type"
    except KeyError as e:
        print(f"Error parsing message: {e}")
        return None, None

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
