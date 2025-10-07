from telebot import TeleBot
from settings import TELEGRAM_TOKEN

bot = TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "¡Funciona el test!")

bot.polling()
