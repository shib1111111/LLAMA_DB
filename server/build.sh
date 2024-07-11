#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy models
#python -m spacy download en_core_web_md
python -m spacy download en_core_web_sm

# Ensure script is executable
chmod +x "${BASH_SOURCE[0]}"

# Check if curl is installed using which
if ! which curl > /dev/null; then
    echo "curl is not installed. Please install curl to proceed."
    exit 1
fi

# Set the Telegram bot webhook
curl -X POST "https://api.telegram.org/bot7384496009:AAFFzZfGjSqihS9s_Akhud8jiwv0_Ac8C0c/setWebhook?url=https://llama-db.onrender.com/telegram/query&drop_pending_updates=True"
