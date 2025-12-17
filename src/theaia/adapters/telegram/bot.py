"""THEA IA Telegram Bot - 100% CONVERSATIONAL (NO COMMANDS)

Full-featured conversational booking bot with:
- Natural language understanding (Groq LLM)
- Tool calling for appointment management
- 24/7 flexible scheduling
- User state management
- BookingAgent integration (per-user GroqTools)
- NO COMMAND MODE - Pure conversational AI
"""

import os
import logging
from datetime import datetime

from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from theaia.core.conversation.llm_client import LLMClient, LLMConfig
from theaia.services.groq_tools import GroqTools
from theaia.services.user_service import UserService
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine
from theaia.agents.booking_agent import BookingAgent

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramBotManager:
    """THEA IA Telegram Bot - 100% conversational, no commands."""

    def __init__(
        self,
        token: str,
        user_service: UserService = None,
        booking_service: BookingService = None,
        availability_engine: AvailabilityEngine = None,
    ):
        """Initialize bot with services.

        Args:
            token: Telegram bot token
            user_service: UserService instance
            booking_service: BookingService instance
            availability_engine: AvailabilityEngine instance
        """
        self.token = token
        self.app = None

        # Check GROQ_API_KEY exists
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env")

        # Initialize Groq client (shared across all users)
        self.groq_client = Groq(api_key=groq_api_key)

        # Initialize services (with defaults if not provided)
        self.user_service = user_service or UserService()
        self.booking_service = booking_service or BookingService()
        self.availability_engine = availability_engine or AvailabilityEngine()

        # Initialize LLMClient (shared for all users)
        logger.info("🧠 Initializing LLMClient...")
        self.llm_client = LLMClient(LLMConfig(model="mixtral-8x7b-32768"))
        logger.info("✅ LLMClient initialized")

        # Store conversation history per user
        self.conversations = {}

        logger.info("🤖 Initializing THEA IA Telegram Bot...")
        logger.info("🧠 Groq LLM ready")
        logger.info("📅 Appointment management enabled")
        logger.info("💬 100% CONVERSATIONAL MODE (NO COMMANDS)")
        logger.info("🤖 BookingAgent will create per-user GroqTools instances")
        self._init_application()

    def _init_application(self):
        """Setup application and handlers."""
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        logger.info("✅ Application initialized")

    def _setup_handlers(self):
        """Register conversational handlers."""
        # ALL messages (including first contact) → conversational handler
        # NO command handlers - pure conversational AI
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        logger.info("✅ Handlers: 100% Conversational mode (no commands) 🛠️")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle ALL text messages with BookingAgent.
        
        - No /start needed
        - First message auto-registers user
        - 100% conversational interaction
        - BookingAgent creates per-user GroqTools
        """
        user = update.effective_user
        user_id = user.id
        user_message = update.message.text

        logger.info(f"📨 {user.first_name} ({user_id}): {user_message}")

        # Initialize conversation if needed
        if user_id not in self.conversations:
            self.conversations[user_id] = []

        try:
            # Auto-register user on first message (no /start needed)
            db_user = self.user_service.get_or_create_user(
                telegram_id=user_id,
                username=user.username or f"user_{user_id}",
                first_name=user.first_name or "",
                last_name=user.last_name or "",
                timezone="Europe/Madrid",
            )
            
            # Update last interaction
            self.user_service.update_last_interaction(user_id)

            # Show typing indicator
            await update.message.chat.send_action("typing")

            # Create per-user GroqTools instance
            groq_tools = GroqTools(
                booking_service=self.booking_service,
                availability_engine=self.availability_engine,
                user_id=user_id,
                groq_client=self.groq_client,
                user_service=self.user_service
            )

            # Create BookingAgent for this user
            booking_agent = BookingAgent(
                user_service=self.user_service,
                booking_service=self.booking_service,
                availability_engine=self.availability_engine,
                groq_tools=groq_tools,
                llm_client=self.llm_client
            )

            # Call BookingAgent with conversation history
            response = await booking_agent.chat(
                user_message=user_message,
                user_id=user_id,
                conversation_history=self.conversations[user_id]
            )

            # Add to conversation history
            self.conversations[user_id].append({"role": "user", "content": user_message})
            self.conversations[user_id].append({"role": "assistant", "content": response})

            # Keep only last 20 messages for context (10 pairs)
            if len(self.conversations[user_id]) > 20:
                self.conversations[user_id] = self.conversations[user_id][-20:]

            # Send response
            if response:
                # Split long responses into multiple messages if needed
                if len(response) > 4096:  # Telegram max message length
                    for i in range(0, len(response), 4096):
                        await update.message.reply_text(response[i : i + 4096])
                else:
                    await update.message.reply_text(response)
            else:
                await update.message.reply_text(
                    "No pude procesar tu solicitud. ¿Puedes repetir?"
                )

            logger.info(f"✅ Response to {user.first_name}: {response[:50]}...")

        except Exception as e:
            logger.error(f"❌ Error handling message: {e}", exc_info=True)
            error_msg = "Disculpa, tuve un problema. ¿Puedes repetir?"
            await update.message.reply_text(error_msg)

    def start(self):
        """Start the bot with polling."""
        logger.info("🚀 Starting THEA IA Telegram Bot...")
        logger.info("💬 100% Conversational mode (NO COMMANDS)")
        logger.info("📅 Appointments 24/7 enabled")
        logger.info("📡 Bot running. Ctrl+C to stop.")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    def stop(self):
        """Stop the bot."""
        logger.info("⏹️ Stopping bot...")


def main():
    """Main entry point."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found")
        return

    bot = TelegramBotManager(token)

    try:
        bot.start()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
    finally:
        bot.stop()


if __name__ == "__main__":
    main()
