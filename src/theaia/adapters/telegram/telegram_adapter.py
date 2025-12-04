"""
TelegramAdapter - THEA IA
Integración Telegram Bot con PostgreSQL Database

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02.2 - Telegram Integration
Actualizado: 03 Dic 2025 - H03 CoreRouter Integration ✅
"""

import asyncio
from typing import Optional, Dict, Any
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from src.theaia.database.session import get_db
from src.theaia.database.repositories import (
    UserRepository,
    ConversationRepository,
    MessageHistoryRepository,
)
from src.theaia.core.router import CoreRouter

class TelegramAdapter:
    """
    Adapter Telegram con persistencia PostgreSQL.
    
    Integra:
    - Telegram Bot API
    - PostgreSQL Database (UserRepository, ConversationRepository, MessageHistoryRepository)
    - CoreRouter (FSM multiagente)
    
    Features:
    - Persistencia usuarios automática (get_or_create)
    - Persistencia conversaciones con FSM state
    - Auditoría completa mensajes (user + bot + intent)
    - Multi-tenant support (tenant_id)
    - Async/await completo
    
    Example:
        adapter = TelegramAdapter(token="YOUR_BOT_TOKEN", tenant_id="default")
        await adapter.start()
    """
    
    def __init__(self, token: str, tenant_id: str = "default"):
        """
        Inicializa TelegramAdapter.
        
        Args:
            token: Bot token de @BotFather
            tenant_id: ID del tenant (default "default")
        """
        self.token = token
        self.tenant_id = tenant_id
        self.application = Application.builder().token(token).build()
        self.router = CoreRouter()
        
        # Registrar handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Registra handlers de comandos y mensajes."""
        # Comandos
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        
        # Mensajes de texto
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler /start - Registra usuario y crea conversación.
        
        Flow:
        1. Extrae datos Telegram del update
        2. get_or_create usuario en PostgreSQL
        3. get_or_create conversación (session_id = telegram_chat_id)
        4. Envía mensaje bienvenida
        5. Guarda mensaje en message_history
        """
        telegram_user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Session para database
        async for session in get_db():
            try:
                # 1. Persistir usuario (get_or_create)
                user_repo = UserRepository(session)
                user, created = await user_repo.get_or_create_from_telegram(
                    telegram_data={
                        "id": telegram_user.id,
                        "username": telegram_user.username,
                        "first_name": telegram_user.first_name,
                        "last_name": telegram_user.last_name,
                        "language_code": telegram_user.language_code,
                    },
                    tenant_id=self.tenant_id
                )
                
                # 2. Crear/obtener conversación
                conv_repo = ConversationRepository(session)
                session_id = f"telegram_{chat_id}"
                conversation, conv_created = await conv_repo.get_or_create(
                    user_id=user.id,
                    tenant_id=self.tenant_id,
                    session_id=session_id,
                    initial_state="idle"
                )
                
                # 3. Mensaje bienvenida
                if created:
                    bot_response = (
                        f"👋 ¡Hola {telegram_user.first_name}!\n\n"
                        "Soy THEA IA, tu asistente personal inteligente.\n\n"
                        "Puedo ayudarte con:\n"
                        "📅 Eventos y recordatorios\n"
                        "📝 Notas y listas\n"
                        "🔍 Consultas y búsquedas\n\n"
                        "Escribe cualquier cosa para empezar."
                    )
                else:
                    bot_response = (
                        f"👋 ¡Bienvenido de nuevo {telegram_user.first_name}!\n\n"
                        "¿En qué puedo ayudarte hoy?"
                    )
                
                await update.message.reply_text(bot_response)
                
                # 4. Auditoría mensaje
                msg_repo = MessageHistoryRepository(session)
                await msg_repo.add_message(
                    conversation_id=conversation.id,
                    tenant_id=self.tenant_id,
                    message_id=f"msg_{update.message.message_id}",
                    user_message="/start",
                    bot_response=bot_response,
                    intent_detected="start_command",
                    confidence_score=1.0
                )
                
                await session.commit()
                
            except Exception as e:
                await session.rollback()
                print(f"❌ Error /start: {e}")
                await update.message.reply_text(
                    "❌ Error al procesar. Intenta de nuevo."
                )
            finally:
                break  # Solo una iteración del generador
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler /help - Muestra ayuda."""
        help_text = """
🤖 **THEA IA - Comandos**

📅 **Eventos:**
- "Crear evento mañana 15:00"
- "Recordarme llamar a María"

📝 **Notas:**
- "Crear nota: Comprar leche"
- "Buscar notas trabajo"

🔍 **Consultas:**
- "¿Qué eventos tengo hoy?"
- "Mostrar mis notas"

⚙️ **Sistema:**
/start - Reiniciar conversación
/help - Mostrar esta ayuda
/reset - Limpiar contexto

Escribe cualquier cosa en lenguaje natural 💬
        """
        await update.message.reply_text(help_text, parse_mode="Markdown")
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler /reset - Limpia contexto conversación."""
        chat_id = update.effective_chat.id
        session_id = f"telegram_{chat_id}"
        
        async for session in get_db():
            try:
                conv_repo = ConversationRepository(session)
                
                # Buscar conversación
                conversation = await conv_repo.get_by_session_id(
                    session_id=session_id,
                    tenant_id=self.tenant_id
                )
                
                if conversation:
                    # Limpiar contexto
                    await conv_repo.clear_context(
                        conversation_id=conversation.id,
                        tenant_id=self.tenant_id
                    )
                    
                    # Resetear estado a idle
                    await conv_repo.update_state(
                        conversation_id=conversation.id,
                        tenant_id=self.tenant_id,
                        new_state="idle"
                    )
                    
                    await session.commit()
                    
                    await update.message.reply_text(
                        "✅ Contexto limpiado. Conversación reiniciada."
                    )
                else:
                    await update.message.reply_text(
                        "⚠️ No hay conversación activa."
                    )
                
            except Exception as e:
                await session.rollback()
                print(f"❌ Error /reset: {e}")
                await update.message.reply_text("❌ Error al resetear.")
            finally:
                break
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handler mensajes de texto - Procesa con CoreRouter + Database.
        
        Flow:
        1. Obtiene usuario + conversación de PostgreSQL
        2. Procesa mensaje con CoreRouter (FSM) ✅ H03 INTEGRADO
        3. Actualiza state conversación
        4. Guarda mensaje + respuesta en message_history
        5. Envía respuesta a Telegram
        """
        telegram_user = update.effective_user
        chat_id = update.effective_chat.id
        user_message = update.message.text
        
        start_time = datetime.now(timezone.utc)
        
        async for session in get_db():
            try:
                # 1. Obtener usuario
                user_repo = UserRepository(session)
                user = await user_repo.get_by_telegram_id(
                    telegram_id=telegram_user.id,
                    tenant_id=self.tenant_id
                )
                
                if not user:
                    # Usuario no registrado, dirigir a /start
                    await update.message.reply_text(
                        "⚠️ Usuario no registrado. Usa /start primero."
                    )
                    return
                
                # 2. Obtener conversación
                conv_repo = ConversationRepository(session)
                session_id = f"telegram_{chat_id}"
                conversation, _ = await conv_repo.get_or_create(
                    user_id=user.id,
                    tenant_id=self.tenant_id,
                    session_id=session_id,
                    initial_state="idle"
                )
                
                # 3. Procesar con CoreRouter (FSM) ✅ H03 INTEGRADO
                current_state = conversation.current_state
                context_data = conversation.context_data or {}
                
                # Procesar con CoreRouter REAL
                router_result = self.router.handle(
                    user_id=str(user.id),
                    message=user_message
                )
                
                # Extraer resultado CoreRouter
                bot_response = router_result["message"]
                new_state = router_result["state"]
                intent_detected = router_result["intent"]
                confidence_score = router_result["confidence"]
                
                # Merge context CoreRouter + Database
                context_data.update(router_result.get("context", {}))
                
                # 4. Actualizar conversación
                await conv_repo.update_state(
                    conversation_id=conversation.id,
                    tenant_id=self.tenant_id,
                    new_state=new_state,
                    context=context_data
                )
                
                # 5. Auditoría mensaje
                end_time = datetime.now(timezone.utc)
                processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
                
                msg_repo = MessageHistoryRepository(session)
                await msg_repo.add_message(
                    conversation_id=conversation.id,
                    tenant_id=self.tenant_id,
                    message_id=f"msg_{update.message.message_id}",
                    user_message=user_message,
                    bot_response=bot_response,
                    intent_detected=intent_detected,
                    confidence_score=confidence_score,
                    processing_time_ms=processing_time_ms
                )
                
                await session.commit()
                
                # 6. Enviar respuesta
                await update.message.reply_text(bot_response)
                
            except Exception as e:
                await session.rollback()
                print(f"❌ Error procesando mensaje: {e}")
                await update.message.reply_text(
                    "❌ Error al procesar tu mensaje. Intenta de nuevo."
                )
            finally:
                break
    
    async def start(self):
        """Inicia el bot (polling)."""
        print("🤖 THEA IA - TelegramAdapter iniciando...")
        print(f"📁 Tenant: {self.tenant_id}")
        print(f"🔗 Database: PostgreSQL conectado")
        print(f"🧠 CoreRouter: 5 agentes MVP cargados")
        print("✅ Bot corriendo...\n")
        
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
    
    async def stop(self):
        """Detiene el bot."""
        print("\n🛑 Deteniendo bot...")
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
        print("✅ Bot detenido")

# Punto de entrada
async def main():
    """Ejecuta TelegramAdapter."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TENANT_ID = os.getenv("TENANT_ID", "default")
    
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado en .env")
        return
    
    adapter = TelegramAdapter(token=BOT_TOKEN, tenant_id=TENANT_ID)
    
    try:
        await adapter.start()
        
        # Mantener corriendo hasta Ctrl+C
        print("Presiona Ctrl+C para detener...")
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupción detectada")
    finally:
        await adapter.stop()

if __name__ == "__main__":
    asyncio.run(main())
