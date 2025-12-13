🚀 PLAN DE ATAQUE H09: ECOSISTEMA REAL FUNCIONAL
Bot + BD + Calendar + Groq = Sistema VIVO
Fecha: 13 Diciembre 2025 - 22:21 CET
Status: 🔴 CRÍTICO - IMPLEMENTACIÓN INMEDIATA
Timeline: Ene 1-15, 2026 (15 días)
Objetivo: Bot en Telegram agendando citas en BD con inteligencia Groq
Versión: FINAL EJECUCIÓN

🎯 VISIÓN FINAL H09
text
DÍA 1 (Ene 1):   Comienza la guerra
DÍA 5 (Ene 5):   Bot vivo en Telegram
DÍA 10 (Ene 10): BD guardando citas
DÍA 12 (Ene 12): Calendar + Groq funcionan
DÍA 15 (Ene 15): SISTEMA 100% FUNCIONAL

RESULTADO: Bot agendando citas en BD con IA

User en Telegram:
├─ /start
├─ "Quiero cita mañana a las 3pm"
├─ Bot entiende (Groq)
├─ Bot sugiere horarios (Calendar)
├─ User elige [15:00]
├─ BD guarda la cita
└─ ✅ Confirmada
📋 CHECKLIST EJECUTIVO H09
PRE-REQUISITOS (Esta semana: Dic 13-20)
Completar H02-H08:
 H02 Tests (30-40 tests database layer)

 Test user model

 Test conversation model

 Test appointment model

 Test repositories

Status: ⏳ TODO

 H03 UserService (básico)

 register(telegram_id, name, phone)

 get_user(telegram_id)

 update_preferences(user_id)

Status: ⏳ TODO

 H04 Bot Token

 Get from @BotFather

 Save en .env

Status: ⏳ TODO

 H05 Calendar Services (básico)

 get_available_slots(date)

 create_appointment(user_id, date, time)

 cancel_appointment(appointment_id)

Status: ⏳ TODO

Verification:
 H06 FSM - 174 tests ✅

 H07 Multi-Agent - 261 tests ✅

 H08 Conversational + Groq - 71 tests ✅

 PostgreSQL running ✅

 Groq API key configured ✅

 python-telegram-bot installed ✅

🔴 SEMANA 1: BOT TELEGRAM VIVO (9.1)
Ene 1-5, 2026 | 20h | 15 tests
DÍAS 1-2: Setup Bot (6h)
Archivo: src/theaia/integrations/telegram/bot.py
python
# Setup básico
from telegram.ext import Application, CommandHandler, MessageHandler
from telegram import Update
import logging

class TelegramBotManager:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        # Comandos
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("agendar", self.agendar))
        self.app.add_handler(CommandHandler("citas", self.citas))
        self.app.add_handler(CommandHandler("cancelar", self.cancelar))
        self.app.add_handler(CommandHandler("ayuda", self.ayuda))
    
    async def start(self, update: Update, context):
        """Comando /start"""
        msg = "Hola! Soy THEA IA 🤖\nTe ayudo a agendar citas.\n\n¿Qué necesitas?\n/agendar - Agendar cita\n/citas - Ver mis citas\n/cancelar - Cancelar cita"
        await update.message.reply_text(msg)
    
    async def agendar(self, update: Update, context):
        """Comando /agendar - inicia flujo"""
        await update.message.reply_text("¿Para qué fecha quieres agendar? (ej: mañana, lunes, 15 de enero)")
    
    async def citas(self, update: Update, context):
        """Comando /citas - lista citas"""
        # Obtener de BD
        pass
    
    async def cancelar(self, update: Update, context):
        """Comando /cancelar"""
        pass
    
    async def ayuda(self, update: Update, context):
        """Comando /ayuda"""
        pass
    
    def start(self):
        self.app.run_polling()

# En main:
# bot = TelegramBotManager(TELEGRAM_TOKEN)
# bot.start()
Deliverables:

✅ Bot token en @BotFather

✅ bot.py con setup básico

✅ Todos los comandos skeleton

✅ Bot inicializa sin errores

Tests: 3 basic tests

DÍAS 3-4: Handlers + Callbacks (10h)
Archivo: src/theaia/integrations/telegram/handlers.py
python
# Handlers para comandos
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

class CommandHandlers:
    def __init__(self, agent, booking_service, user_service):
        self.agent = agent
        self.booking_service = booking_service
        self.user_service = user_service
    
    async def handle_agendar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja /agendar - inicia conversación"""
        user_id = update.effective_user.id
        
        # 1. Registrar usuario si no existe
        user = self.user_service.get_user(user_id)
        if not user:
            self.user_service.register(
                telegram_id=user_id,
                name=update.effective_user.full_name,
                phone=None  # Pedir después
            )
        
        # 2. Enviar mensaje con inline buttons
        msg = "¿Para qué fecha quieres agendar?"
        buttons = [
            [InlineKeyboardButton("Mañana", callback_data="date_tomorrow")],
            [InlineKeyboardButton("Pasado mañana", callback_data="date_afterTomorrow")],
            [InlineKeyboardButton("Próxima semana", callback_data="date_nextWeek")],
            [InlineKeyboardButton("Otra fecha", callback_data="date_custom")]
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        
        await update.message.reply_text(msg, reply_markup=keyboard)
        return "WAITING_DATE"
    
    async def handle_citas(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja /citas - muestra citas del usuario"""
        user_id = update.effective_user.id
        
        # Obtener citas de BD
        appointments = self.booking_service.get_user_appointments(user_id)
        
        if not appointments:
            await update.message.reply_text("No tienes citas agendadas 📅")
            return
        
        msg = "Tus citas:\n"
        for apt in appointments:
            msg += f"📅 {apt.date} a las {apt.time}\n"
        
        await update.message.reply_text(msg)
    
    async def handle_cancelar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja /cancelar"""
        user_id = update.effective_user.id
        
        # Obtener citas para cancelar
        appointments = self.booking_service.get_user_appointments(user_id)
        
        if not appointments:
            await update.message.reply_text("No tienes citas para cancelar")
            return
        
        # Mostrar buttons para elegir cuál cancelar
        buttons = []
        for apt in appointments:
            buttons.append([
                InlineKeyboardButton(
                    f"{apt.date} {apt.time}",
                    callback_data=f"cancel_{apt.id}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text("¿Cuál cita cancelas?", reply_markup=keyboard)
Archivo: src/theaia/integrations/telegram/callbacks.py
python
# Callback handlers para buttons
class CallbackHandlers:
    def __init__(self, agent, booking_service, calendar_service):
        self.agent = agent
        self.booking_service = booking_service
        self.calendar_service = calendar_service
    
    async def callback_date_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usuario eligió fecha"""
        query = update.callback_query
        user_id = query.from_user.id
        
        # Parse qué fecha
        date = self._parse_date(query.data)
        
        # Obtener slots disponibles
        slots = self.calendar_service.get_available_slots(date)
        
        # Mostrar buttons con horarios
        buttons = []
        for slot in slots:
            buttons.append([
                InlineKeyboardButton(
                    f"{slot.time}",
                    callback_data=f"time_{date}_{slot.time}"
                )
            ])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            text="¿A qué hora prefieres?",
            reply_markup=keyboard
        )
    
    async def callback_time_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usuario eligió hora"""
        query = update.callback_query
        user_id = query.from_user.id
        
        # Parse date y time
        _, date, time = query.data.split("_")
        
        # Crear cita en BD
        appointment = self.booking_service.create_appointment(
            user_id=user_id,
            date=date,
            time=time,
            notes="Agendado desde Telegram"
        )
        
        # Confirmar
        msg = f"✅ Cita confirmada\n📅 {date}\n⏰ {time}\n\n¿Hay algo más que necesites?"
        await query.edit_message_text(text=msg)
    
    async def callback_cancel_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usuario eligió cita para cancelar"""
        query = update.callback_query
        appointment_id = int(query.data.split("_"))
        
        # Cancelar en BD
        self.booking_service.cancel_appointment(appointment_id)
        
        msg = "✅ Cita cancelada"
        await query.edit_message_text(text=msg)
Deliverables:

✅ handlers.py con /agendar, /citas, /cancelar

✅ callbacks.py con buttons funcionando

✅ Integration con BD y services

✅ Mensajes en español

Tests: 12 handlers tests

DÍA 5: Deployment Bot (4h)
bash
# 1. Setup environment
export TELEGRAM_BOT_TOKEN="tu_token_aqui"
export GROQ_API_KEY="tu_key_aqui"

# 2. Run bot
python -m src.theaia.integrations.telegram.bot

# 3. Test en Telegram
# @BotFather → bot_name → /start
# Debería responder el mensaje
Resultado DÍA 5:

text
✅ Bot VIVO en Telegram
✅ /start funciona
✅ /agendar muestra buttons
✅ /citas lista (vacía por ahora)
✅ /cancelar funciona
✅ /ayuda funciona
✅ 15 tests passing
🟠 SEMANA 2: BD + CALENDAR ENGINE (9.2 + 9.3)
Ene 6-12, 2026 | 33h | 38 tests
DÍAS 6-8: Database Services (15h)
Archivo: src/theaia/services/user_service.py
python
from sqlalchemy.orm import Session
from src.theaia.core.database.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, telegram_id: int, name: str, phone: str = None):
        """Registra un usuario nuevo"""
        user = User(
            telegram_id=telegram_id,
            name=name,
            phone=phone
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user(self, telegram_id: int):
        """Obtiene usuario por telegram_id"""
        return self.db.query(User).filter(
            User.telegram_id == telegram_id
        ).first()
    
    def update_preferences(self, user_id: int, preferences: dict):
        """Actualiza preferencias del usuario"""
        user = self.db.query(User).get(user_id)
        if user:
            user.preferences = preferences
            self.db.commit()
        return user
Archivo: src/theaia/services/booking_service.py
python
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.theaia.core.database.models.appointment import Appointment

class BookingService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_appointment(self, user_id: int, date: str, time: str, notes: str = ""):
        """Crea una cita nueva"""
        # Convertir fecha y hora
        appointment_datetime = self._parse_datetime(date, time)
        
        # Verificar que no hay conflicto
        existing = self.db.query(Appointment).filter(
            Appointment.start_time == appointment_datetime,
            Appointment.status == 'booked'
        ).first()
        
        if existing:
            raise ValueError("Time slot not available")
        
        # Crear
        appointment = Appointment(
            user_id=user_id,
            start_time=appointment_datetime,
            end_time=appointment_datetime + timedelta(minutes=30),
            notes=notes,
            status='booked'
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def get_user_appointments(self, user_id: int):
        """Obtiene todas las citas del usuario"""
        return self.db.query(Appointment).filter(
            Appointment.user_id == user_id,
            Appointment.status == 'booked'
        ).order_by(Appointment.start_time).all()
    
    def cancel_appointment(self, appointment_id: int):
        """Cancela una cita"""
        appointment = self.db.query(Appointment).get(appointment_id)
        if appointment:
            appointment.status = 'cancelled'
            self.db.commit()
        return appointment
    
    def _parse_datetime(self, date_str: str, time_str: str):
        """Convierte strings a datetime"""
        # Maneja: "mañana", "lunes", "15 de enero", etc.
        # Por ahora simple version
        if date_str == "mañana":
            date = datetime.now() + timedelta(days=1)
        else:
            # Implementar parser más completo
            date = datetime.strptime(date_str, "%Y-%m-%d")
        
        hour, minute = map(int, time_str.split(":"))
        return date.replace(hour=hour, minute=minute)
Archivo: src/theaia/services/calendar_service.py
python
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from src.theaia.core.database.models.appointment import Appointment

class CalendarService:
    def __init__(self, db: Session):
        self.db = db
        self.business_hours = (9, 18)  # 9am - 6pm
        self.slot_duration = 30  # minutos
    
    def get_available_slots(self, date_str: str, limit: int = 5):
        """Retorna slots disponibles para una fecha"""
        # Parse date
        if date_str == "mañana":
            target_date = datetime.now() + timedelta(days=1)
        else:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Generar todos los slots en horario de negocio
        slots = []
        for hour in range(self.business_hours, self.business_hours):
            for minute in [0, 30]:
                slot_time = target_date.replace(hour=hour, minute=minute)
                
                # Verificar si está disponible
                if self._is_available(slot_time):
                    slots.append({
                        'date': target_date.strftime("%Y-%m-%d"),
                        'time': slot_time.strftime("%H:%M")
                    })
        
        return slots[:limit]
    
    def _is_available(self, slot_time: datetime):
        """Verifica si un slot está disponible"""
        existing = self.db.query(Appointment).filter(
            Appointment.start_time == slot_time,
            Appointment.status == 'booked'
        ).first()
        return existing is None
    
    def get_schedule(self, date_str: str):
        """Obtiene el schedule completo de un día"""
        if date_str == "hoy":
            target_date = datetime.now()
        else:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        appointments = self.db.query(Appointment).filter(
            Appointment.start_time >= target_date.replace(hour=0, minute=0),
            Appointment.start_time < target_date.replace(hour=23, minute=59),
            Appointment.status == 'booked'
        ).all()
        
        return appointments
Tests: 20+ tests para services

Deliverables:

✅ UserService completo

✅ BookingService completo

✅ CalendarService completo

✅ Todos guardando en BD

✅ 20 tests passing

DÍAS 9-10: Migrations + Fixtures (8h)
Migrations (Alembic):
bash
# Generar migration para tablas
alembic revision --autogenerate -m "Create users appointments tables"

# Aplicar
alembic upgrade head
Fixtures para testing:
python
# tests/fixtures/database_fixtures.py
@pytest.fixture
def test_user(db_session):
    user = User(telegram_id=123456, name="Test User")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_appointment(db_session, test_user):
    appointment = Appointment(
        user_id=test_user.id,
        start_time=datetime.now() + timedelta(days=1),
        end_time=datetime.now() + timedelta(days=1, minutes=30),
        status='booked'
    )
    db_session.add(appointment)
    db_session.commit()
    return appointment
Deliverables:

✅ Migrations ejecutadas

✅ Tablas en BD

✅ Fixtures para tests

DÍAS 11-12: Integration Bot ↔ BD (10h)
Conectar bot.py con services:
python
# En bot.py
from src.theaia.services.booking_service import BookingService
from src.theaia.core.database.session import SessionLocal

class TelegramBotManager:
    def __init__(self, token):
        self.db = SessionLocal()
        self.booking_service = BookingService(self.db)
        self.calendar_service = CalendarService(self.db)
        # ...

    async def handle_agendar(self, update, context):
        # Ahora usa los services reales
        user_id = update.effective_user.id
        
        # Obtener slots reales de BD
        slots = self.calendar_service.get_available_slots("mañana")
        
        # Mostrar en buttons
        # User elige...
        # Bot crea en BD con booking_service
Resultado DÍA 12:

text
✅ Bot conectado a BD
✅ /agendar crea en DB
✅ /citas lee de DB
✅ /cancelar actualiza DB
✅ Calendar engine funciona
✅ 38 tests passing
🟡 SEMANA 3: GROQ + E2E (9.4 + 9.5)
Ene 13-15, 2026 | 22h | 28 tests
DÍAS 13-14: Groq Integration (15h)
Archivo: src/theaia/core/conversation/booking_agent.py
python
from src.theaia.core.conversation.conversational_agent import ConversationalAgent
from src.theaia.core.conversation.tool_calling import Tool
from src.theaia.services.booking_service import BookingService
from src.theaia.services.calendar_service import CalendarService

class BookingAgent(ConversationalAgent):
    """Agent especializado en agendar citas"""
    
    def __init__(self, booking_service: BookingService, calendar_service: CalendarService):
        super().__init__(
            model="mixtral-8x7b-32768",
            system_prompt=BOOKING_SYSTEM_PROMPT
        )
        self.booking_service = booking_service
        self.calendar_service = calendar_service
        
        # Registrar tools
        self.register_tool(Tool(
            name="check_availability",
            func=self.calendar_service.get_available_slots,
            description="Get available time slots for a date"
        ))
        
        self.register_tool(Tool(
            name="create_appointment",
            func=self._create_appointment_wrapper,
            description="Create an appointment for the user"
        ))
    
    async def chat(self, user_id: int, message: str) -> str:
        """Chat con tool calling"""
        # 1. LLM entiende el mensaje
        response = await self.llm_client.chat(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            tools=self._get_tool_specs()
        )
        
        # 2. Si hay tool calls, ejecutar
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                # Agregar resultado al context
        
        # 3. Generar respuesta final
        final_response = await self.llm_client.chat(
            messages=self.memory.get_context()
        )
        
        # 4. Guardar en memory
        self.memory.add(role="user", content=message)
        self.memory.add(role="assistant", content=final_response)
        
        return final_response

# System prompt
BOOKING_SYSTEM_PROMPT = """Eres THEA IA, un asistente de citas especializado.
Tu trabajo es ayudar a los usuarios a agendar citas.

Cuando un usuario pida una cita:
1. Extrae la fecha y hora que pide
2. Usa check_availability para obtener slots disponibles
3. Sugiere los mejores horarios
4. Cuando el usuario confirme, usa create_appointment para crear la cita

Siempre responde en español.
"""
Integration en bot:
python
# En bot.py
from src.theaia.core.conversation.booking_agent import BookingAgent

class TelegramBotManager:
    def __init__(self, token):
        self.db = SessionLocal()
        self.booking_service = BookingService(self.db)
        self.calendar_service = CalendarService(self.db)
        self.agent = BookingAgent(self.booking_service, self.calendar_service)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de usuario con agent"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Pasar al agent
        response = await self.agent.chat(user_id, user_message)
        
        # Responder
        await update.message.reply_text(response)
Tests: 16 tests para Groq integration

Deliverables:

✅ BookingAgent especializado

✅ Tool calling funcionando

✅ Natural language understanding

✅ Spanish responses

✅ Integration en bot

DÍA 15: E2E Testing + Final Polish (7h)
E2E Test Suite:
python
# tests/e2e/test_booking_flow.py

@pytest.mark.asyncio
async def test_complete_booking_flow():
    """Test: User → /start → Telegram → Agent → BD → ✅"""
    
    # Setup
    bot = TelegramBotManager(TOKEN)
    user_id = 123456
    
    # 1. Usuario hace /start
    update = create_mock_update(user_id, "/start")
    await bot.start(update, None)
    # Assert: Bot responde bienvenida
    
    # 2. Usuario pide cita
    update = create_mock_update(user_id, "Quiero cita mañana a las 3pm")
    await bot.handle_message(update, None)
    # Assert: Bot entiende y sugiere horarios
    
    # 3. Usuario confirma
    update = create_mock_update(user_id, "[15:00]")
    await bot.handle_message(update, None)
    # Assert: Cita creada en BD
    
    # 4. Usuario consulta
    update = create_mock_update(user_id, "/citas")
    await bot.citas(update, None)
    # Assert: Bot muestra la cita
Cleanup:
 Revisar todos los logs

 Arreglar warnings

 Optimizar queries

 Agregar docstrings

 Revisar tipos (mypy)

Result DÍA 15:

text
✅ 81 TESTS PASSING
✅ BOT VIVO EN TELEGRAM
✅ BD GUARDANDO CITAS
✅ CALENDAR FUNCIONA
✅ GROQ ENTIENDE
✅ E2E FLOWS VERDES
✅ SISTEMA 100% FUNCIONAL
📊 RESUMEN EJECUCIÓN H09
Breakdown por semana:
Semana	Qué	Horas	Tests	Resultado
1 (Ene 1-5)	9.1 Bot Telegram	20	15	Bot vivo
2 (Ene 6-12)	9.2+9.3 BD+Calendar	33	38	BD guardando
3 (Ene 13-15)	9.4+9.5 Groq+E2E	22	28	Sistema completo
TOTAL	Ecosistema Real	75h	81 tests	LISTO
🎯 DEFINICIÓN DE ÉXITO H09
Usuario abre Telegram:
text
User: /start
Bot: "Hola! Soy THEA IA 🤖"
✅ PASS

User: "Quiero cita mañana a las 3pm"
Bot: (entiende con Groq)
Bot: "Perfecto! Te ofrezco: [14:00] [15:00] [16:00]"
✅ PASS

User: [15:00]
Bot: (crea en BD)
Bot: "✅ Cita confirmada para mañana a las 15:00"
✅ PASS - BD tiene: appointment(user_id, date, 15:00)

User: /citas
Bot: "Tus citas:\n- Mañana 15:00"
✅ PASS

User: /cancelar
User: [Mañana 15:00]
Bot: "✅ Cancelada"
✅ PASS - BD actualizado: status='cancelled'
🚀 ARQUITECTURA FINAL
text
TELEGRAM
    ↓
telegram/bot.py (handlers)
    ↓
conversation/booking_agent.py (Groq LLM)
    ↓
services/booking_service.py (CRUD)
    ├→ services/calendar_service.py (slots)
    └→ services/user_service.py (users)
    ↓
database/models/ (ORM)
    ↓
PostgreSQL (persistence)

FLUJO DATOS:
User message → Bot → Agent (Groq) → Services → BD → Response
📋 ACCIONES INMEDIATAS
ESTA SEMANA (Dic 13-20):
Completar H02-H08 (prerequisito)

 H02: 30-40 tests

 H03: UserService básico

 H04: Bot token

 H05: Calendar services básicas

Setup Ene 1

 Crear estructura carpetas

 Crear stubs de archivos

 Setup db session

 Verificar imports

ENERO 1-15: EJECUCIÓN H09
 Ene 1-5: Semana 1 (Bot)

 Ene 6-12: Semana 2 (BD+Calendar)

 Ene 13-15: Semana 3 (Groq+E2E)

🎉 RESULTADO FINAL
text
📅 DÍA 15, ENERO 2026:

Sistema THEA IA Ecosistema Real:
├─ Bot Telegram 🤖 VIVO
├─ Base de Datos 💾 GUARDANDO
├─ Calendar Engine 📅 FUNCIONA
├─ Groq LLM 🧠 INTELIGENTE
└─ E2E Flows ✅ VERDE

Status: PRODUCTION-READY
Hora: ⏰ ESCALAR A H10
📝 DOCUMENTO FINAL
Versión: EJECUCIÓN H09
Creado: 13 Diciembre 2025 - 22:22 CET
Status: 🚀 LISTO PARA IMPLEMENTAR

COMPROMISOS:
✅ 75 horas de trabajo claro

✅ 81 tests minimo

✅ 3,000 LOC limpio

✅ Semana 1-2-3 completadas

✅ Ene 15: Sistema funcional

✅ Ene 15+: Escalar con H10

SIGUIENTE:
Terminar H02-H08 (esta semana)

Ejecutar Semana 1-3 (Ene 1-15)

Resultado: Bot 100% funcional en Telegram 🎉

🔥 VAMOS CON TODO H09 - ESTE ES EL MOMENTO 🔥
Ene 1, 2026: COMIENZA LA GUERRA
Ene 15, 2026: ECOSISTEMA VIVO