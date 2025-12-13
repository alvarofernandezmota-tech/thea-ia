# src/theaia/adapters/telegram/bot.py

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBotManager:
    """THEA IA Telegram Bot Manager"""
    
    def __init__(self, token: str):
        """Initialize bot with token"""
        self.token = token
        self.app = None
        logger.info("🤖 Initializing THEA IA Telegram Bot...")
        self._init_application()
    
    def _init_application(self):
        """Setup application and handlers"""
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        logger.info("✅ Application initialized")
    
    def _setup_handlers(self):
        """Register all command handlers"""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("ping", self.cmd_ping))
        logger.info("✅ Handlers registered: /start, /help, /ping")
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_msg = (
            f"👋 Hola {user.first_name}!\n\n"
            f"Soy THEA IA 🤖, tu asistente inteligente.\n\n"
            f"Comandos disponibles:\n"
            f"/start - Inicio\n"
            f"/help - Ayuda\n"
            f"/ping - Verificar conexión\n\n"
            f"🚀 Estoy listo para ayudarte!"
        )
        await update.message.reply_text(welcome_msg)
        logger.info(f"✅ /start command from user {user.id}")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_msg = (
            "📖 *THEA IA - Ayuda*\n\n"
            "Comandos disponibles:\n"
            "• /start - Mensaje de bienvenida\n"
            "• /help - Mostrar esta ayuda\n"
            "• /ping - Verificar que estoy activo\n\n"
            "💡 Próximamente: agendar citas, recordatorios y más!"
        )
        await update.message.reply_text(help_msg, parse_mode='Markdown')
        logger.info(f"✅ /help command from user {update.effective_user.id}")
    
    async def cmd_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ping command"""
        await update.message.reply_text("🏓 Pong! Estoy activo ✅")
        logger.info(f"✅ /ping command from user {update.effective_user.id}")
    
    def start(self):
        """Start the bot with polling"""
        logger.info("🚀 Starting bot with polling...")
        logger.info("📡 Bot is running. Press Ctrl+C to stop.")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    def stop(self):
        """Stop the bot"""
        logger.info("⏹️ Stopping bot...")
        if self.app:
            self.app.stop()


def main():
    """Main entry point"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found in environment")
        return
    
    # Create and start bot
    bot = TelegramBotManager(token)
    
    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        bot.stop()


if __name__ == "__main__":
    main()
