from fastapi import APIRouter, HTTPException, Depends,Request,BackgroundTasks
from sqlalchemy.orm import Session
from models import User,ApiKey
from database import get_db
from api_utils import get_current_user
from schemas import ConnectRequest,QueryRequest
from llm_utils import init_database,get_response
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from telegram_utils import message_parser,send_message_telegram
import asyncpg 


api_router = APIRouter()


user_db_connections = {}
@api_router.post("/connect")
def connect(request: ConnectRequest, current_user: User = Depends(get_current_user)):
    try:
        db_conn = init_database(request.user, request.password, request.host, request.port, request.database)
        user_db_connections[current_user.id] = db_conn 
        return {"message": "Connected to database successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/query")
def query(request: QueryRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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


@api_router.post('/whatsapp/query', response_class=PlainTextResponse)
async def whatsapp_query(request: Request):
    try:
        db_conn = init_database(
            "indian_data_user", 
            "rP5vYYjVDtskMuTmodSSop7V3N2LRrGu", 
            "dpg-cpom45iju9rs738ra2ug-a.oregon-postgres.render.com",
            "5432", 
            "indian_data"
        )
        chat_history = []

        form = await request.form()
        incoming_query = form.get('Body', '').lower()
        print("Question: ", incoming_query)
        answer = get_response(incoming_query, db_conn, chat_history)
        print("BOT Answer: ", answer)
        bot_resp = MessagingResponse()
        bot_resp.message(str(answer))

    except asyncpg.PostgresError as e:
        print("Database error:", e)
        bot_resp = MessagingResponse()
        bot_resp.message("Sorry, there was a problem connecting to the database.")
    except Exception as e:
        print("Error:", e)
        bot_resp = MessagingResponse()
        bot_resp.message("Sorry, an error occurred while processing your request.")    
        
    return str(bot_resp)

@api_router.post("/telegram/query")
async def telegram_query(request: Request):
    try:
        db_conn = init_database(
            "indian_data_user", 
            "rP5vYYjVDtskMuTmodSSop7V3N2LRrGu", 
            "dpg-cpom45iju9rs738ra2ug-a.oregon-postgres.render.com",
            "5432", 
            "indian_data"
        )
        chat_history = []

        msg = await request.json()
        chat_id, incoming_query = message_parser(msg)
        answer = get_response(incoming_query, db_conn, chat_history)
        send_message_telegram(chat_id, answer)
        
        return {"message": "Message sent successfully"}
    
    except asyncpg.PostgresError as e:
        print("Database error:", e)
        return HTTPException(status_code=500, detail="Database error")
    
    except Exception as e:
        print("Error:", e)
        return HTTPException(status_code=500, detail="An error occurred while processing the request")
