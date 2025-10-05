from telebot import TeleBot
bot = TeleBot('8297680422:AAGhueCQccdmc4vhVUma0lj6mL0p8h1OorI')
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "¡Funciona el test!")
bot.polling()
