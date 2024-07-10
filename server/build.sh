#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_md
python -m spacy download en_core_web_sm


# Ensure script is executable
chmod +x "${BASH_SOURCE[0]}"
