from telebot import TeleBot
from settings import TELEGRAM_TOKEN
bot = TeleBot(TELEGRAM_TOKEN)

from thea.core.scheduler_agent import SchedulerAgent


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "¡Hola! Soy THEA, tu asistente de agendamiento de citas.")

@bot.message_handler(func=lambda m: 'agendar' in m.text.lower())
def agendar_cita_handler(message):
    user_id = message.from_user.id
    agent = SchedulerAgent(user_id)
    evento = agent.agendar_cita("mañana", "11:00", "Revisión")
    bot.reply_to(message, f"{evento}")

@bot.message_handler(func=lambda m: 'consultar' in m.text.lower())
def consultar_citas_handler(message):
    user_id = message.from_user.id
    agent = SchedulerAgent(user_id)
    citas = agent.consultar_citas()
    bot.reply_to(message, "\n".join(citas))

bot.polling()
