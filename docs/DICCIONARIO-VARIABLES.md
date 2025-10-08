# DICCIONARIO DE VARIABLES - THEA IA 2.0

## 🔧 Variables de Entorno (.env)

### Configuración Base de Datos
```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/theaia_db
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=theaia_db
DATABASE_USER=theaia_user
DATABASE_PASSWORD=secure_password

# Redis (opcional - para caché)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=redis_password
REDIS_DB=0
```

### Integración Telegram
```bash
# Bot Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook/telegram
TELEGRAM_WEBHOOK_SECRET=webhook_secret_key
```

### Configuración Aplicación
```bash
# Entorno
ENVIRONMENT=development  # development, staging, production
DEBUG=true
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# API
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1
SECRET_KEY=your_super_secret_key_here
```

### Machine Learning / NLP
```bash
# Modelos ML
SPACY_MODEL=es_core_news_sm
INTENT_MODEL_PATH=models/intent_classifier.pkl
ENTITY_MODEL_PATH=models/entity_extractor.pkl
ML_CONFIDENCE_THRESHOLD=0.8
```

### Monitoreo y Logging
```bash
# Logging
LOG_FILE_PATH=logs/theaia.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# Métricas
PROMETHEUS_PORT=9090
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
```

### Configuración Externa
```bash
# Google Calendar (opcional)
GOOGLE_CALENDAR_CREDENTIALS_PATH=credentials/google_calendar.json
GOOGLE_CALENDAR_SCOPES=https://www.googleapis.com/auth/calendar

# Notificaciones
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=notifications@theaia.com
EMAIL_PASSWORD=email_app_password
```

---

## 📊 Diccionario Estados FSM

### Estados Principales
```python
STATES = {
    'IDLE': 'Usuario inactivo, esperando interacción',
    'LISTENING': 'Bot escuchando comando del usuario',
    'PROCESSING': 'Procesando e interpretando solicitud',
    'CONFIRMING': 'Esperando confirmación del usuario',
    'EXECUTING': 'Ejecutando acción confirmada',
    'ERROR': 'Estado de error, requiere intervención',
    'HELP': 'Modo ayuda, proporcionando información'
}
```

### Transiciones
```python
TRANSITIONS = [
    ['start', 'IDLE', 'LISTENING'],
    ['process', 'LISTENING', 'PROCESSING'],
    ['confirm', 'PROCESSING', 'CONFIRMING'],
    ['execute', 'CONFIRMING', 'EXECUTING'],
    ['complete', 'EXECUTING', 'IDLE'],
    ['error', '*', 'ERROR'],
    ['reset', '*', 'IDLE'],
    ['help', '*', 'HELP']
]
```

---

## 🎯 Diccionario Intenciones (NLP)

### Intenciones Eventos
```python
EVENT_INTENTS = {
    'create_event': [
        'crear evento', 'nueva cita', 'agendar', 'programar',
        'recordarme', 'tengo reunión', 'cita médica'
    ],
    'list_events': [
        'qué tengo hoy', 'agenda', 'eventos', 'citas programadas',
        'qué tengo mañana', 'horario'
    ],
    'modify_event': [
        'cambiar cita', 'modificar evento', 'mover reunión',
        'reagendar', 'cambiar hora'
    ],
    'cancel_event': [
        'cancelar cita', 'eliminar evento', 'borrar reunión',
        'anular cita'
    ]
}
```

### Intenciones Notas
```python
NOTE_INTENTS = {
    'create_note': [
        'apunta', 'nota', 'recordatorio', 'anota que',
        'guarda esto', 'no olvides'
    ],
    'list_notes': [
        'mis notas', 'qué apunté', 'recordatorios',
        'lista notas'
    ],
    'search_notes': [
        'busca nota', 'encuentra', 'dónde apunté'
    ]
}
```

### Entidades Temporales
```python
TEMPORAL_ENTITIES = {
    'time_expressions': [
        'hoy', 'mañana', 'pasado mañana', 'esta semana',
        'próximo lunes', 'en 2 horas', 'a las 15:00'
    ],
    'duration_expressions': [
        '1 hora', '30 minutos', 'todo el día', 'media jornada'
    ],
    'frequency_expressions': [
        'diario', 'semanal', 'cada lunes', 'mensual'
    ]
}
```

---

## 🔤 Diccionario Respuestas Bot

### Confirmaciones
```python
CONFIRMATIONS = {
    'event_created': '✅ Evento creado: {event_title} el {date} a las {time}',
    'event_modified': '✏️ Evento modificado exitosamente',
    'event_cancelled': '❌ Evento cancelado: {event_title}',
    'note_saved': '📝 Nota guardada: {note_preview}',
    'confirmation_request': '❓ ¿Confirmas esta acción? Responde Sí/No'
}
```

### Errores
```python
ERROR_MESSAGES = {
    'invalid_date': '⚠️ Fecha no válida. Usa formato: DD/MM/YYYY HH:MM',
    'event_not_found': '❌ No encontré ese evento en tu agenda',
    'db_error': '💥 Error de base de datos. Intenta más tarde',
    'intent_not_understood': '🤔 No entendí tu solicitud. ¿Puedes reformularla?',
    'missing_information': '❓ Falta información: {missing_fields}'
}
```

### Ayuda
```python
HELP_MESSAGES = {
    'welcome': '👋 ¡Hola! Soy Thea IA. Puedo ayudarte con eventos y notas.',
    'commands': """
🗓️ **Eventos:**
- "Recordarme reunión mañana 15:00"
- "¿Qué tengo hoy?"
- "Cancelar cita médica"

📝 **Notas:**
- "Apunta: comprar leche"
- "Mis notas"
- "Busca nota sobre proyecto"
    """,
    'examples': '💡 **Ejemplos:** ...'
}
```