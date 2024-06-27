from fastapi import FastAPI, Request, HTTPException, BackgroundTasks,APIRouter
from pydantic import BaseModel
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import asyncpg
api_router = APIRouter()

TOKEN = "7273450268:AAEUX058yj_etHpOKe-Lo62W-7si_mJCt8c"
bot = Bot(token=TOKEN)


user_sessions = {}


class TelegramWebhookRequest(BaseModel):
    update_id: int
    message: dict

async def handle_update(update: Update):
    if update.message:
        user_id = update.message.from_user.id
        user_input = update.message.text

        if user_id not in user_sessions:
            await send_welcome_message(update)
            return

        session = user_sessions[user_id]
        step = session.get("step")

        if user_input.lower() == "stop":
            if "db_conn" in session:
                await session["db_conn"].close()
            user_sessions.pop(user_id, None)
            await update.message.reply_text("Connection closed.")
            return

        if step == "host":
            session["host"] = user_input
            session["step"] = "port"
            await update.message.reply_text("Please enter your database port:")
        elif step == "port":
            session["port"] = user_input
            session["step"] = "database"
            await update.message.reply_text("Please enter your database name:")
        elif step == "database":
            session["database"] = user_input
            session["step"] = "user"
            await update.message.reply_text("Please enter your database username:")
        elif step == "user":
            session["user"] = user_input
            session["step"] = "password"
            await update.message.reply_text("Please enter your database password:")
        elif step == "password":
            session["password"] = user_input
            try:
                db_conn = await asyncpg.connect(
                    user=session["user"],
                    password=session["password"],
                    database=session["database"],
                    host=session["host"],
                    port=session["port"]
                )
                session["db_conn"] = db_conn
                session["step"] = "query"
                await update.message.reply_text("Database connected successfully. Please enter your query:")
            except asyncpg.PostgresError as e:
                await update.message.reply_text(f"Database connection failed: {e}")
        elif step == "query":
            db_conn = session.get("db_conn")
            try:
                result = await db_conn.fetch(user_input)
                await update.message.reply_text(f"Query result: {result}")
            except asyncpg.PostgresError as e:
                await update.message.reply_text(f"Query failed: {e}")

async def send_welcome_message(update: Update):
    await update.message.reply_text("Hello, welcome to Llama Db. Please enter your database host:")
    user_sessions[update.message.from_user.id] = {
        "step": "host"
    }



@api_router.post("/telegram/webhook")
async def telegram_webhook(update: TelegramWebhookRequest, background_tasks: BackgroundTasks):
    update = Update.de_json(update.dict(), bot)
    background_tasks.add_task(handle_update, update)
    return "ok"



