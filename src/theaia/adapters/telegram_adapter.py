# src/theaia/adapters/telegram_adapter.py

import logging
from aiogram import Dispatcher
from aiogram.types import Message
from theaia.core.router import process_user_input

async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text

    response, _ = await process_user_input(user_id, text)
    await message.answer(response)


# Configura el logger para este módulo
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def handle_message(message: Message):
    """
    Handler que responde a cualquier mensaje recibido.
    Registra el mensaje y envía una respuesta con el nombre del usuario.
    """
    logger.info(f"Received message: chat_id={message.chat.id} text={message.text}")
    await message.answer(f"¡Hola, {message.from_user.first_name}!")

def register_handlers(dp: Dispatcher):
    """
    Registra todos los handlers de Telegram en el Dispatcher.
    """
    dp.message.register(handle_message)
