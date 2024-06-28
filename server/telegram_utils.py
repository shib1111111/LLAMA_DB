import requests
from fastapi import FastAPI, Request, Response
from config import TELEGRAM_SECRET_KEY

telegram_token = TELEGRAM_SECRET_KEY

# To Get Chat ID and message which is sent by client
def message_parser(message):
    try:
        chat_id = message['message']['chat']['id']
        text = message['message']['text']
        print("Chat ID: ", chat_id)
        print("Message: ", text)
        return chat_id, text
    except KeyError as e:
        print(f"Error parsing message: {e}")
        return None, None

# To send message using "SendMessage" API
def send_message_telegram(chat_id, text):
    try:
        url = f'https://api.telegram.org/bot{token}/sendMessage'
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
