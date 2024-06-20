from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User,ApiKey
from database import get_db
from api_utils import get_current_user
from schemas import ConnectRequest,QueryRequest
from llm_utils import init_database,get_response

api_router = APIRouter()


user_db_connections = {}
@api_router.post("/connect")
def connect(request: ConnectRequest, current_user: User = Depends(get_current_user)):
    #global db_conn
    try:
        db_conn = init_database(request.user, request.password, request.host, request.port, request.database)
        user_db_connections[current_user.id] = db_conn 
        return {"message": "Connected to database successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/query")
def query(request: QueryRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    #global db_conn
    db_conn = user_db_connections.get(current_user.id)
    api_key_entry = db.query(ApiKey).filter(ApiKey.key == request.api_key).first()
    if not api_key_entry:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if db_conn is None:
        raise HTTPException(status_code=400, detail="Database not connected")
    try:
        response = get_response(request.query, db_conn, request.chat_history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
