📅 Agent: Agenda — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🔴 Alta (Core)

📋 Propósito
El Agente Agenda gestiona eventos, reuniones y calendarios del usuario. Es responsable de crear, listar, modificar y eliminar eventos integrándose con APIs de calendario externas.

Audiencia:

Desarrolladores integrando funcionalidad de eventos

QA testeando flujos de agenda

Usuarios finales usando comandos de calendario

🎯 Responsabilidades
Funcionalidad	Descripción
Crear evento	Crear nuevo evento con título, fecha, hora, participantes
Listar eventos	Mostrar eventos por rango de fechas
Modificar evento	Actualizar título, fecha, hora, asistentes
Eliminar evento	Borrar evento por ID
Buscar eventos	Búsqueda por palabra clave o fecha
Recordatorios	Configurar notificaciones previas
🔧 Configuración
Archivo: config/agents/agenda.yaml

text
agent:
  name: "Agenda"
  version: "1.0"
  enabled: true
  timeout: 30
  max_retries: 3

capabilities:
  - create_event
  - list_events
  - modify_event
  - delete_event
  - search_events
  - set_reminder

models:
  nlp: "bert-base-uncased"
  date_parser: "dateutil"

database:
  table: "events"
  cache_ttl: 3600

external_apis:
  google_calendar:
    enabled: true
    credentials_path: "/secrets/google_calendar_creds.json"
    timeout: 10
  
  outlook_calendar:
    enabled: false
    credentials_path: "/secrets/outlook_creds.json"
📥 Entrada esperada
Formato general
python
{
  "action": "create_event",  # create/list/modify/delete/search
  "data": {
    "title": "Reunión equipo",
    "date": "2025-11-09",
    "time": "10:00",
    "duration": 60,  # minutos
    "attendees": ["user@example.com"],
    "description": "Discutir roadmap Q1",
    "location": "Sala A",
    "reminder": 15  # minutos antes
  }
}
Casos específicos
Crear evento:

python
{
  "action": "create_event",
  "data": {
    "title": "Reunión",
    "date": "2025-11-09",
    "time": "10:00"
  }
}
Listar eventos:

python
{
  "action": "list_events",
  "data": {
    "start_date": "2025-11-08",
    "end_date": "2025-11-15"
  }
}
Modificar evento:

python
{
  "action": "modify_event",
  "data": {
    "event_id": "evt_12345",
    "title": "Nuevo título",
    "time": "11:00"
  }
}
📤 Salida esperada
Éxito
python
{
  "status": "success",
  "action": "create_event",
  "event": {
    "event_id": "evt_12345",
    "title": "Reunión equipo",
    "date": "2025-11-09",
    "time": "10:00",
    "duration": 60,
    "attendees": ["user@example.com"],
    "reminder": 15,
    "url": "https://calendar.google.com/event?id=evt_12345"
  },
  "message": "Evento creado exitosamente"
}
Error
python
{
  "status": "error",
  "action": "create_event",
  "error_code": "INVALID_DATE",
  "message": "Fecha no válida: debe ser YYYY-MM-DD",
  "details": {
    "input": "invalid_date",
    "expected": "YYYY-MM-DD"
  }
}
🔄 Flujo de procesamiento
1. Crear evento
text
Usuario input
     ↓
Validar entrada (título, fecha, hora)
     ↓
Parsear fecha/hora con dateutil
     ↓
Verificar conflictos de horario
     ↓
Crear evento en BD local
     ↓
Sincronizar con API externa (Google Calendar)
     ↓
Configurar recordatorio (si aplica)
     ↓
Retornar evento creado + URL
2. Listar eventos
text
Usuario input (rango de fechas)
     ↓
Validar fechas
     ↓
Consultar BD local (cache)
     ↓
Si cache miss: consultar API externa
     ↓
Filtrar por rango de fechas
     ↓
Ordenar por fecha/hora
     ↓
Retornar lista de eventos
🧠 Lógica interna
Parseo de fechas natural
El agente entiende lenguaje natural:

python
"mañana a las 10"         → 2025-11-09 10:00
"próximo lunes 15:00"     → 2025-11-11 15:00
"en 2 horas"              → 2025-11-08 18:47
"el 15 de diciembre"      → 2025-12-15 (hora default 09:00)
Implementación:

python
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

def parse_natural_date(text):
    # Maneja casos comunes
    if "mañana" in text:
        return datetime.now() + timedelta(days=1)
    return parse(text, fuzzy=True)
Detección de conflictos
python
def check_conflicts(start_time, end_time):
    # Consultar eventos existentes
    existing = db.query(Event).filter(
        Event.start_time.between(start_time, end_time)
    ).all()
    
    if existing:
        return {
            "conflict": True,
            "conflicting_events": existing
        }
    return {"conflict": False}
🔗 Integraciones
Google Calendar API
python
from googleapiclient.discovery import build

def sync_to_google_calendar(event_data):
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': event_data['title'],
        'start': {
            'dateTime': event_data['datetime'].isoformat(),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': (event_data['datetime'] + timedelta(minutes=event_data['duration'])).isoformat(),
            'timeZone': 'Europe/Madrid',
        }
    }
    
    result = service.events().insert(calendarId='primary', body=event).execute()
    return result['id']
📊 Métricas
Métrica	Actual	Target
Response time	450ms	< 500ms
Success rate	97%	> 95%
API sync rate	95%	> 90%
Conflict detection accuracy	98%	> 95%
🚨 Errores comunes
Error	Causa	Solución
INVALID_DATE	Formato fecha incorrecto	Usar YYYY-MM-DD
INVALID_TIME	Formato hora incorrecto	Usar HH:MM (24h)
CONFLICT_DETECTED	Evento solapado	Modificar horario
API_TIMEOUT	Google Calendar no responde	Retry automático
EVENT_NOT_FOUND	ID evento no existe	Verificar event_id
✅ Tests
Unit test ejemplo
python
def test_agenda_create_event_valid_data():
    agent = AgendaAgent()
    
    result = agent.process({
        "action": "create_event",
        "data": {
            "title": "Test event",
            "date": "2025-11-09",
            "time": "10:00"
        }
    })
    
    assert result["status"] == "success"
    assert result["event"]["title"] == "Test event"
    assert "event_id" in result["event"]
Ver más tests en: src/theaia/tests/unit/test_agents_agenda.py

🔗 Enlaces relacionados
Agents Overview — Sistema multi-agente

Best Practices — Convenciones

Testing — Cómo testear agentes

📌 Meta-información
Campo	Valor
Archivo	docs/agents/agent_agenda.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	Agents Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.3 (docs/agents/)

Agente core con prioridad alta

Integración validada con Google Calendar

Tests unitarios y de integración completos

Validado en sesión 35

8/10/25. 16.46

