# server/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "sqlite:///user.db"

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
