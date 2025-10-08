import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from theaia.adapters.telegram_adapter import register_handlers
import logging

# 1. Carga .env y logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USE_POLLING    = os.getenv("TELEGRAM_USE_POLLING", "false").lower() == "true"
API_HOST       = os.getenv("API_HOST", "0.0.0.0")
API_PORT       = int(os.getenv("API_PORT", 8000))
WEBHOOK_URL    = os.getenv("TELEGRAM_WEBHOOK_URL", "")
WEBHOOK_PATH   = WEBHOOK_URL.replace("https://", "").replace("http://", "")
WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")

# 2. Instancia bot y dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
register_handlers(dp)

# 3. Crea FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    if USE_POLLING:
        logger.info("Starting Telegram long polling…")
        asyncio.create_task(dp.start_polling(bot, skip_updates=True))
    else:
        await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post(f"/{WEBHOOK_PATH}")
async def telegram_webhook(request: Request):
    if WEBHOOK_SECRET and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(403, "Forbidden")
    update = Update(**await request.json())
    await dp.process_update(update)
    return {"ok": True}
