# src/theaia/adapters/telegram/bot.py

import os
import logging
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes
)

# Import Groq LLM client
from theaia.core.conversation.llm_client import LLMClient, LLMConfig

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBotManager:
    """THEA IA Conversational Telegram Bot"""
    
    def __init__(self, token: str):
        """Initialize conversational bot"""
        self.token = token
        self.app = None
        
        # Check GROQ_API_KEY exists
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env")
        
        # Initialize LLM with correct config
        config = LLMConfig(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500
        )
        
        self.llm = LLMClient(config)
        
        # Store conversation history per user
        self.conversations = {}
        
        logger.info("🤖 Initializing THEA IA Conversational Bot...")
        logger.info("🧠 Groq LLM ready")
        self._init_application()
    
    def _get_system_prompt(self) -> str:
        """System prompt for conversational booking"""
        return """Eres THEA IA, un asistente virtual amigable y profesional para agendar citas.

PERSONALIDAD:
- Amigable pero profesional
- Español natural de España
- Conciso y claro
- Usa emojis ocasionalmente (📅, ✅, ⏰, 👋)

CAPACIDADES:
- Entender intenciones en lenguaje natural
- Ayudar a agendar citas
- Responder preguntas sobre citas
- Confirmar y cancelar citas

FORMATO DE RESPUESTA:
- Máximo 2-3 líneas
- Directo al punto
- Pregunta solo lo necesario

EJEMPLOS:

User: "Hola"
You: "¡Hola! 👋 Soy THEA IA. ¿En qué puedo ayudarte?"

User: "Quiero una cita"
You: "Perfecto. ¿Para qué día? 📅"

User: "Mañana a las 3"
You: "Mañana a las 15:00. ¿Lo confirmo? ✅"

User: "Sí"
You: "✅ Cita agendada para mañana 14 dic a las 15:00"

User: "¿Qué citas tengo?"
You: "Tienes 1 cita: Mañana 14 dic, 15:00"

IMPORTANTE:
- NO uses comandos como /start o /help
- Conversación natural SIEMPRE
- Si no entiendes, pregunta
- Confirma antes de agendar
"""
    
    def _init_application(self):
        """Setup application and handlers"""
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        logger.info("✅ Application initialized")
    
    def _setup_handlers(self):
        """Register conversational handlers"""
        # /start command (only for first greeting)
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        
        # ALL text messages → conversational handler
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
        
        logger.info("✅ Handlers: conversational mode 💬")
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start - first greeting"""
        user = update.effective_user
        user_id = user.id
        
        # Initialize conversation
        self.conversations[user_id] = []
        
        welcome = (
            f"👋 ¡Hola {user.first_name}!\n\n"
            f"Soy THEA IA, tu asistente personal.\n\n"
            f"Háblame de forma natural:\n"
            f'• "Quiero agendar una cita"\n'
            f'• "¿Qué citas tengo?"\n'
            f'• "Cancela mi cita de mañana"\n\n'
            f"¿En qué puedo ayudarte? 😊"
        )
        
        await update.message.reply_text(welcome)
        logger.info(f"✅ /start from user {user_id} ({user.first_name})")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages with Groq"""
        user = update.effective_user
        user_id = user.id
        user_message = update.message.text
        
        logger.info(f"📨 {user.first_name} ({user_id}): {user_message}")
        
        # Initialize conversation if needed
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        try:
            # Show typing indicator
            await update.message.chat.send_action("typing")
            
            # Get response from Groq using the chat method
            response = await self.llm.chat(
                message=user_message,
                system_prompt=self._get_system_prompt()
            )
            
            # Send response
            await update.message.reply_text(response)
            
            logger.info(f"✅ Response to {user.first_name}: {response[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            error_msg = "Disculpa, tuve un problema. ¿Puedes repetir?"
            await update.message.reply_text(error_msg)
    
    def start(self):
        """Start the bot with polling"""
        logger.info("🚀 Starting conversational bot...")
        logger.info("💬 Natural language mode active")
        logger.info("📡 Bot running. Ctrl+C to stop.")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def stop(self):
        """Stop the bot"""
        logger.info("⏹️ Stopping bot...")


def main():
    """Main entry point"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found")
        return
    
    bot = TelegramBotManager(token)
    
    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.stop()


if __name__ == "__main__":
    main()
