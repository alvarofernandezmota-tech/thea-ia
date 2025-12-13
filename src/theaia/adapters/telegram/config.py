# src/theaia/adapters/telegram/config.py

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramConfig:
    """Telegram Bot Configuration"""
    
    # Bot credentials
    bot_token: str
    
    # Mode settings
    use_polling: bool = True
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    
    # Bot behavior
    parse_mode: str = "Markdown"  # or "HTML"
    timeout: int = 30
    
    # Rate limiting
    rate_limit_messages: int = 30  # messages per minute
    rate_limit_window: int = 60  # seconds
    
    # Commands
    commands = {
        "start": "Iniciar conversación con THEA IA",
        "help": "Mostrar ayuda y comandos disponibles",
        "ping": "Verificar que el bot está activo",
        "agendar": "Agendar una nueva cita",
        "citas": "Ver mis citas agendadas",
        "cancelar": "Cancelar una cita"
    }
    
    @classmethod
    def from_env(cls) -> "TelegramConfig":
        """Create config from environment variables"""
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment")
        
        return cls(
            bot_token=token,
            use_polling=os.getenv("TELEGRAM_USE_POLLING", "true").lower() == "true",
            webhook_url=os.getenv("TELEGRAM_WEBHOOK_URL"),
            webhook_secret=os.getenv("TELEGRAM_WEBHOOK_SECRET")
        )


# Messages templates
MESSAGES = {
    "welcome": """👋 Hola {first_name}!

Soy THEA IA 🤖, tu asistente inteligente.

Comandos disponibles:
/start - Inicio
/help - Ayuda
/ping - Verificar conexión
/agendar - Agendar cita
/citas - Ver mis citas
/cancelar - Cancelar cita

🚀 Estoy listo para ayudarte!""",
    
    "help": """📖 *THEA IA - Ayuda*

*Comandos disponibles:*
• /start - Mensaje de bienvenida
• /help - Mostrar esta ayuda
• /ping - Verificar que estoy activo
• /agendar - Agendar una nueva cita
• /citas - Ver tus citas agendadas
• /cancelar - Cancelar una cita

💡 Próximamente: recordatorios automáticos y más!""",
    
    "ping": "🏓 Pong! Estoy activo ✅",
    
    "error": "❌ Error: {error}",
    
    "unknown_command": "❓ Comando desconocido. Usa /help para ver los comandos disponibles."
}


# Button labels
BUTTONS = {
    "date_tomorrow": "Mañana",
    "date_after_tomorrow": "Pasado mañana",
    "date_next_week": "Próxima semana",
    "date_custom": "Otra fecha",
    "confirm": "✅ Confirmar",
    "cancel": "❌ Cancelar",
    "back": "◀️ Volver"
}


# Logging format
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
