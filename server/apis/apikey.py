import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import APIKeyResponse,APIKeyListResponse
from database import get_db
from api_utils import get_current_user
from models import ApiKey,User

apikey_router = APIRouter()

@apikey_router.post("/api_key", response_model=APIKeyResponse)
def generate_api_key(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_api_key = ApiKey(key=str(uuid.uuid4()), user_id=current_user.id)
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    return {"api_key": new_api_key.key}

@apikey_router.get("/api_keys", response_model=APIKeyListResponse)
def list_api_keys(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    api_keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    keys = [api_key.key for api_key in api_keys]
    return {"api_keys": keys}