🎯 ROADMAP REVISADO: PRIORIDAD ECOSISTEMA REAL
Telegram Bot + BD + Calendar + Groq = Sistema Funcional
Fecha: 13 Diciembre 2025
Status: 🔴 CRÍTICO - Replaneamiento ejecutivo
Versión: 3.0 - ECOSISTEMA FIRST

📊 CAMBIO DE ESTRATEGIA
ANTES: Web/App primero
text
H09: Web UI (React) ❌ INCORRECTO
├─ Frontend bonito
├─ Pero sin datos reales
└─ Complementario, no core
AHORA: Ecosistema primero ✅ CORRECTO
text
H09: ECOSISTEMA REAL FUNCIONAL ✅ PRIORIDAD
├─ Bot Telegram VIVO
├─ BD GUARDANDO datos
├─ Calendar ENGINE funcionando
├─ Groq LLM entendiendo
└─ Todo INTEGRADO y TESTEABLE

Web/App: DESPUÉS (complementario)
├─ Cuando tengamos datos
├─ Para visualizar lo que existe
└─ Mejor UX, no core
🎯 ROADMAP H02-H17 REORDENADO
FASE 1: MVP FUNCIONAL (H02-H08) ✅ EN CURSO
Período: Dic 13 - Dic 24, 2025

Hito	Período	Status	Horas	Tests
H02	Nov-Dic	✅ PARTIAL	80	0
H03	Nov-Dic	❌ TODO	40	0
H04	Nov-Dic	❌ TODO	50	0
H05	Nov-Dic	❌ TODO	60	0
H06	Nov-Dic	✅ DONE	120	174
H07	Nov-Dic	✅ DONE	150	261
H08	Nov-Dic	✅ DONE	40	71
Total Fase 1: 540 horas, 506 tests, 12,300 LOC

FASE 2: ECOSISTEMA REAL (H09) 🔴 CRÍTICA
Período: Ene 1-15, 2026 (15 días, 75 horas)

OBJETIVO: Bot funcionando + BD + Calendar + Groq

Submódulo	Horas	Tests	LOC	Prioridad
9.1 Bot Telegram	20	15	800	🔴 CRÍTICA
9.2 Database Services	15	20	600	🔴 CRÍTICA
9.3 Calendar Engine	18	18	700	🔴 CRÍTICA
9.4 Groq Integration	15	16	600	🔴 CRÍTICA
9.5 E2E Integration	7	12	300	🔴 CRÍTICA
Total H09: 75 horas, 81 tests, 3,000 LOC

FASE 3: ESCALABILIDAD (H10-H14)
Período: Ene 15 - Abr 10, 2026 (85 días, 400 horas)

Hito	Período	Horas	Tests	Foco
H10	Ene 15-29	70	40	Auth + OAuth2
H11	Ene 30-Feb 15	80	45	API Gateway + K8s
H12	Feb 16-Mar 5	70	40	Agent Plugins
H13	Mar 6-25	75	45	Data Pipeline
H14	Mar 26-Abr 10	85	50	Optimization
Total H10-H14: 380 horas, 220 tests

FASE 4: COMPLEMENTARIOS (H15+)
Período: Abr 11 - Jun 1, 2026 (50 días, 240 horas)

Hito	Período	Horas	Tests	Foco
H15	Abr 11-25	65	40	Security + Compliance
H16	Abr 26-May 15	75	45	Monitoring + APM
H17-WEB	May 16-31	80	50	Web UI (si es necesario)
H18-APP	Jun 1+	80	50	Mobile App (si es necesario)
Total H15+: 300 horas, 185 tests

🔴 FASE 2 (H09): ECOSISTEMA REAL - DETALLES
9.1: Bot Telegram COMPLETO (20h)
python
# Objetivo: Bot vivo agendando citas

Comandos:
/start              → Bienvenida + registro
/agendar            → Iniciar flujo booking
/citas              → Ver mis citas
/cancelar          → Cancelar cita
/ayuda             → Help

Flujo usuario:
1. /start
   Bot: "Hola, soy THEA IA. ¿Cómo puedo ayudarte?"
   
2. /agendar
   Usuario: "Quiero una cita mañana"
   Bot: (Llama a Groq) → entiende intent
   Bot: (Llama a Calendar) → obtiene slots
   Bot: "Te ofrezco: [14:00] [15:00] [16:00]"
   
3. Usuario presiona: [14:00]
   Bot: (Llama a BookingService) → crea en BD
   Bot: "✅ Cita confirmada para mañana a las 14:00"
   
4. /citas
   Bot: (Llama a DB) → obtiene citas
   Bot: "Tus citas:\n- Mañana 14:00\n- Jueves 10:00"
   
5. /cancelar
   Bot: "¿Cuál cita cancelas? [Mañana 14:00] [Jueves 10:00]"
   Usuario: [Mañana 14:00]
   Bot: "✅ Cancelada"

Arquitectura:
├─ src/theaia/integrations/telegram/
│  ├─ bot.py (init + dispatcher)
│  ├─ handlers.py (command handlers)
│  ├─ callbacks.py (button callbacks)
│  ├─ middleware.py (auth + logging)
│  └─ states.py (FSM states)
├─ tests/integration/telegram/
│  ├─ test_bot.py
│  ├─ test_handlers.py
│  └─ test_callbacks.py
Deliverables:

✅ Bot token de @BotFather

✅ Comandos implementados

✅ Spanish messages

✅ 15+ tests

✅ Listo en Telegram

9.2: Database Services (15h)
python
# Objetivo: Guardar datos reales en BD

Servicios necesarios:

class UserService:
    def register(telegram_id, name, phone)
        → INSERT INTO users
        → return User
    
    def get_user(telegram_id)
        → SELECT FROM users
        → return User or None
    
    def update_preferences(user_id, prefs)
        → UPDATE users SET preferences
        → return User

class BookingService:
    def create_appointment(user_id, date, time, notes)
        → validate availability
        → INSERT INTO appointments
        → return Appointment
    
    def get_user_appointments(user_id)
        → SELECT FROM appointments WHERE user_id
        → return List[Appointment]
    
    def cancel_appointment(appointment_id)
        → UPDATE appointments SET status='cancelled'
        → return Appointment
    
    def check_conflict(date, time)
        → SELECT FROM appointments WHERE date AND time
        → return bool

class CalendarService:
    def get_available_slots(date)
        → SELECT available slots for date
        → return List[TimeSlot]
    
    def get_schedule(date)
        → SELECT all appointments for date
        → return Dict[TimeSlot, Appointment]

Tablas:
users:
├─ id (PK)
├─ telegram_id (unique)
├─ name
├─ phone
├─ created_at
└─ preferences (JSON)

appointments:
├─ id (PK)
├─ user_id (FK)
├─ start_time
├─ end_time
├─ notes
├─ status (booked/cancelled/completed)
├─ created_at
└─ updated_at

availability:
├─ id (PK)
├─ date
├─ time_slot
├─ available (bool)
└─ updated_at

messages:
├─ id (PK)
├─ user_id (FK)
├─ chat_id (telegram)
├─ message
└─ timestamp

Migrations (Alembic):
- Create users table
- Create appointments table
- Create availability table
- Create messages table
- Add indexes on date, user_id
Deliverables:

✅ 3 services implementados

✅ 4 tablas en BD

✅ Migrations en Alembic

✅ 20+ tests

✅ Fixtures para testing

9.3: Calendar Engine (18h)
python
# Objetivo: Lógica de disponibilidad

class AvailabilityEngine:
    def get_available_slots(date: date) -> List[TimeSlot]:
        """Retorna slots disponibles para una fecha"""
        business_hours = (9, 18)  # 9am - 6pm
        slot_duration = 30  # 30 min slots
        
        # 1. Generate all slots in business hours
        slots = []
        for hour in range(business_hours, business_hours):
            for minute in [0, 30]:
                slots.append(TimeSlot(hour, minute))
        
        # 2. Remove already booked
        booked = db.query(Appointment).filter(
            Appointment.date == date,
            Appointment.status == 'booked'
        ).all()
        
        for appointment in booked:
            slots = [s for s in slots if not s.overlaps(appointment)]
        
        # 3. Return next 5 available
        return slots[:5]
    
    def check_availability(date: date, time: time) -> bool:
        """Verifica si un slot está disponible"""
        existing = db.query(Appointment).filter(
            Appointment.date == date,
            Appointment.start_time == time,
            Appointment.status == 'booked'
        ).first()
        return existing is None
    
    def create_appointment(
        user_id: int, 
        date: date, 
        time: time,
        notes: str
    ) -> Appointment:
        """Crea una cita (después de validar)"""
        if not self.check_availability(date, time):
            raise ConflictError("Time slot not available")
        
        appointment = Appointment(
            user_id=user_id,
            date=date,
            start_time=time,
            end_time=time + timedelta(minutes=30),
            notes=notes,
            status='booked'
        )
        db.add(appointment)
        db.commit()
        return appointment
    
    def cancel_appointment(appointment_id: int) -> Appointment:
        """Cancela una cita"""
        appointment = db.query(Appointment).get(appointment_id)
        if not appointment:
            raise NotFoundError("Appointment not found")
        
        appointment.status = 'cancelled'
        appointment.updated_at = datetime.now()
        db.commit()
        return appointment

# Handling especiales:
- Timezone aware (UTC → user timezone)
- No overbooking (mutex locks)
- Business hours config
- Holiday handling (future)
- Recurring appointments (future)
Deliverables:

✅ Availability engine

✅ Slot generation

✅ Conflict detection

✅ 18+ tests

✅ Timezone support

9.4: Groq LLM Integration (15h)
python
# Objetivo: Agent entiende natural language

class BookingAgent(ConversationalAgent):
    """Agent especializado en booking"""
    
    def __init__(self):
        super().__init__(
            model="mixtral-8x7b-32768",
            system_prompt=BOOKING_SYSTEM_PROMPT
        )
        self.tools = [
            Tool(
                name="check_availability",
                func=calendar_service.get_available_slots,
                description="Get available slots for a date"
            ),
            Tool(
                name="create_appointment",
                func=booking_service.create_appointment,
                description="Create an appointment"
            ),
            Tool(
                name="cancel_appointment",
                func=booking_service.cancel_appointment,
                description="Cancel an appointment"
            ),
            Tool(
                name="get_my_appointments",
                func=booking_service.get_user_appointments,
                description="Get user's appointments"
            ),
        ]
    
    async def chat(self, user_id: int, message: str) -> str:
        """Chat flow con tool calling"""
        
        # 1. Parse intent
        # User: "Quiero agendar una cita mañana a las 3pm"
        # LLM: intent=BOOK, date=tomorrow, time=15:00
        
        response = await self.llm_client.chat(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            tools=self.tools
        )
        
        # 2. Check if LLM wants to call a tool
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                # Execute tool
                result = self._execute_tool(tool_name, args)
                
                # Add result to context
                self.memory.add(
                    role="assistant",
                    content=f"Called {tool_name}: {result}"
                )
        
        # 3. Generate final response
        final_response = await self.llm_client.chat(
            messages=self.memory.get_context()
        )
        
        # 4. Save to memory
        self.memory.add(role="user", content=message)
        self.memory.add(role="assistant", content=final_response)
        
        return final_response

# Intents que entiende:
BOOK_APPOINTMENT:
  "Quiero agendar una cita mañana"
  "¿Puedo reservar el lunes a las 10?"
  → call: check_availability + create_appointment

CANCEL_APPOINTMENT:
  "Quiero cancelar mi cita"
  "¿Puedo cancelar para mañana?"
  → call: get_my_appointments + cancel_appointment

VIEW_APPOINTMENTS:
  "¿Cuáles son mis citas?"
  "Muéstrame mis reservas"
  → call: get_my_appointments

CHECK_AVAILABILITY:
  "¿Tienes disponibilidad mañana?"
  "¿Qué horarios hay el viernes?"
  → call: check_availability
Deliverables:

✅ BookingAgent especializado

✅ Tool calling implementado

✅ Intent parsing

✅ 16+ tests

✅ Spanish responses

9.5: E2E Integration (7h)
python
# Objetivo: Todo junto funcionando

Telegram Flow:
┌─────────────────────────────────────────┐
│ 1. User en Telegram                     │
│    /agendar                             │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. Bot recibe update                    │
│    handlers.command_agendar()           │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. Agent.chat(user_id, "/agendar")     │
│    user_message = "Quiero cita mañana"  │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. Groq LLM entiende intent             │
│    → BOOK_APPOINTMENT                   │
│    → date=tomorrow, time=any            │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. Tool: check_availability(tomorrow)   │
│    → CalendarService.get_slots()        │
│    → [14:00, 15:00, 16:00, 17:00]       │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 6. Format response con buttons          │
│    "Slots disponibles: [14:00] [15:00]" │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 7. Bot.send_message() a Telegram       │
│    Con inline buttons                   │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 8. User presiona [14:00]                │
│    callback_appointment()               │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 9. Tool: create_appointment()           │
│    → BookingService.create()            │
│    → INSERT INTO appointments           │
└─────────────┬───────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 10. Confirmación                        │
│     "✅ Cita confirmada para mañana    │
│      a las 14:00"                       │
└─────────────────────────────────────────┘

Archivos:
├─ src/theaia/integrations/telegram/
│  └─ coordinator.py (orchestrates flow)
├─ tests/e2e/
│  ├─ test_booking_flow.py
│  ├─ test_cancel_flow.py
│  └─ test_view_appointments.py
Deliverables:

✅ E2E flow working

✅ Full integration tested

✅ 12+ E2E tests

✅ Error handling

✅ Production ready

✅ H09 COMPLETADO = SISTEMA FUNCIONAL
Después de H09:

text
Bot en Telegram ✅
├─ Usuario puede agendar
├─ Citas se guardan en BD
├─ Calendar funciona
├─ Groq entiende requests
└─ TODO INTEGRADO Y TESTEABLE

Result:
- 75 horas de trabajo
- 81+ tests passing
- 3,000 LOC
- Sistema 100% funcional
- Listo para exteriorizaciones
📊 FASE 2 vs FASE 3+
H09: Ecosistema Real
text
Prioridad: 🔴 CRÍTICA
Impacto: Sistema funcional
Tests: 81+
Timeline: 15 días
Status: Bot vivo, BD guardando
H10-H14: Escalabilidad
text
Prioridad: 🟡 IMPORTANTE
Impacto: Robustez
Tests: 220+
Timeline: 85 días
Status: Cuando H09 esté done
H15+: Complementarios
text
Prioridad: 🟢 DESEABLE
Impacto: UX/Monitoring
Tests: 185+
Timeline: 50 días
Status: Web/App después si es needed
🎯 DECISIÓN CRÍTICA
❌ NO HACER:
Web UI bonita sin datos

App mobile sin backend

Interfaces vacías

Empezar por UI

✅ HACER:
Bot Telegram VIVO

BD GUARDANDO datos reales

Calendar ENGINE funcionando

Groq LLM inteligente

TODO INTEGRADO

⏰ DESPUÉS (si es needed):
Web UI para visualizar BD

Mobile app para consultar

Dashboard para analytics

Integraciones externas

📌 CONCLUSIÓN
H09 = Poner el ecosistema a funcionar

Bot + BD + Calendar + Groq

75 horas de trabajo real

81+ tests garantizando calidad

Sistema production-ready

Listo en 15 días

Web/App = Después

Cuando tengamos datos que mostrar

Cuando el bot esté proven

Como complemento, no core

Si realmente es necesario

Filosofía:

text
Ecosistema Funcional > Interfaces Bonitas
Datos Reales > Mockups
Bot Proven > Web Vaporware
Sistema Integrado > Componentes sueltos
Versión: 3.0 ECOSISTEMA FIRST
Creado: 13 Diciembre 2025 - 22:12 CET
Status: 🔴 CRÍTICO - Listo para implementar
Enfoque: TELEGRAM BOT + BD + CALENDAR + GROQ = SISTEMA REAL
Siguiente: Implementar H09 (15 días, 75 horas)