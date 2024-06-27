# Pydantic models
from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class APIKeyResponse(BaseModel):
    api_key: str

class APIKeyListResponse(BaseModel):
    api_keys: List[str]

class ConnectRequest(BaseModel):
    user: str
    password: str
    host: str
    port: str
    database: str

class QueryRequest(BaseModel):
    api_key: str
    query: str
    chat_history: Optional[List[dict]] = []
'''
class TelegramWebhookRequest(BaseModel):
    update_id: int
    message: dict
'''
