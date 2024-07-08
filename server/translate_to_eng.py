import requests

def translate_to_english(text, target_language='en'):
  url = "https://translate.googleapis.com/translate_a/single"
  params = {
      'client': 'gtx',
      'sl': 'auto',  
      'tl': target_language,
      'dt': ['t', 'ld'],
      'q': text
  }
  response = requests.get(url, params=params)
  
  if response.status_code == 200:
    translated_text = response.json()[0][0][0] if response.json()[0] else None
    detected_language = response.json()[2] 
    if detected_language != target_language and translated_text:
        return translated_text
    else:
        return text 
  else:
    return text