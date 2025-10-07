# THEA IA – Asistente de Agendamiento Inteligente
#
# Thea IA es un chatbot en Python para Telegram que automatiza el ciclo completo de gestión 
# de citas y eventos con lenguaje natural, integraciones y recordatorios.
#
# 🚀 Funcionalidades Principales
# - Agendar citas y eventos (intake inteligente, validaciones, recordatorios opcionales)
# - Consultar eventos (todos, próximos, pasados)
# - Modificar citas por ID (fecha, duración, título)
# - Cancelar eventos con confirmación
# - Historial de conversación y logs para auditoría
# - Automatizaciones programadas (notificaciones y tareas periódicas)
# - Integraciones configurables con servicios externos
#
# 📁 Estructura del Proyecto
# .
# ├── telegram_theaiabot.py      # Script principal del bot (Application builder)
# ├── db_connection.py           # Función conectar_db() para PostgreSQL
# ├── requirements.txt           # Dependencias del proyecto
# ├── README.md                  # Documentación principal (este archivo)
# ├── TABLAS.md                  # Descripción detallada de cada tabla
# ├── thea/
# │   ├── core/                  # Modelos SQLAlchemy y lógica de negocio
# │   ├── integrations/          # Módulos de conexión con APIs externas
# │   ├── automations/           # Definición de tareas programadas
# │   ├── utils/                 # Funciones de utilidades
# │   └── …
# └── scripts/
#     └── create_tables.py       # Script de migración con SQLAlchemy Base.metadata.create_all(engine)
#
# 📦 Dependencias
# - Python 3.10+
# - python-telegram-bot ≥ 20.0
# - dateparser ≥ 1.1.0
# - psycopg2-binary ≥ 2.9.0
#
# Instalación
# python -m venv venv
# source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate      # Windows
# pip install -r requirements.txt
#
# requirements.txt
# python-telegram-bot>=20.0
# dateparser>=1.1.0
# psycopg2-binary>=2.9.0
#
# 🔧 Configuración
# 1. Clona el repositorio y entra en la carpeta:
#    git clone https://github.com/tuusuario/thea-ia.git
#    cd thea-ia
# 2. Configura tu token de Telegram en telegram_theaiabot.py:
#    TOKEN = "TU_TOKEN_DE_BOTFATHER"
# 3. (Opcional) Ejecuta migraciones de SQLAlchemy:
#    python scripts/create_tables.py
# 4. Inicia el bot:
#    python telegram_theaiabot.py
#
# 🗄️ Base de Datos
# Se usan 9 tablas en PostgreSQL bajo el esquema public. Consulta TABLAS.md para la descripción completa.
# | Tabla             | Función                                                   |
# |-------------------|-----------------------------------------------------------|
# | usuarios          | Registro de usuarios de Telegram                          |
# | conversaciones    | Historial de mensajes (usuario ↔ bot)                     |
# | citas             | Eventos agendados (fecha, duración, estado, usuario)      |
# | historial_citas   | Registro de cambios y eventos históricos de cada cita     |
# | servicios         | Catálogo de servicios o tipos de eventos                  |
# | mensajes_sistema  | Plantillas de mensajes y textos configurables             |
# | integraciones     | Configuración de conexiones con APIs externas             |
# | automatizaciones  | Definición de tareas programadas y notificaciones         |
# | logs              | Auditoría de sucesos y errores internos del sistema       |
#
# 📑 Historial de Desarrollo
# 1. Estructura inicial
#    - Definición de modelo de datos (SQLAlchemy) y tablas fundamentales.
#    - Implementación de db_connection.py.
# 2. Flujo de “Agendar” avanzada
#    - Intake inteligente con detección de intención y extracción de fecha/título.
#    - Validaciones de título, fecha futura, duración.
#    - Confirmación explícita y detección de solapamientos.
#    - Recordatorios previos y en el momento con JobQueue.
# 3. Ayuda contextual
#    - Mensaje de bienvenida informativo ante mensajes sueltos.
#    - Control de errores: reintentos guiados tras múltiples fallos.
#    - Fallback general con ejemplos claros.
# 4. Modularización de flujos
#    - Handlers y funciones específicas para agendar, consultar, modificar, cancelar.
#    - Diccionario centralizado MESSAGES para gestionar textos.
# 5. Extensión de base de datos
#    - Añadidas tablas: historial_citas, servicios, mensajes_sistema, integraciones, automatizaciones, logs.
#    - Script de migración con Base.metadata.create_all(engine).
# 6. Documentación y pruebas
#    - Creación de README.md y TABLAS.md.
#    - Pruebas de flujo completas: agendar, consultar, modificar, cancelar.
#    - Verificación de integridad y migraciones.
#
# 🚀 Uso Rápido
# - Agendar:
#    agendar dentista mañana 10:00
#    o escribe agendar y sigue las indicaciones.
# - Consultar:
#    consultar
#    consultar próximos
#    consultar pasados
# - Modificar:
#    modificar evento 12
# - Cancelar:
#    cancelar evento 15
# - Ayuda:
#    ayuda


🗄️ Variables de la Base de Datos
A continuación se listan todas las tablas y sus columnas tal como se definieron en el proyecto:

1. usuarios
id (SERIAL, NO NULL): Identificador único del usuario

nombre (TEXT, NULL): Nombre mostrado en Telegram

email (TEXT, NO NULL): Email ficticio <user_id>@telegram.com (clave única)

2. conversaciones
id (SERIAL, NO NULL): Identificador único de registro

usuario_id (INT, NO NULL): FK → usuarios.id

mensaje (TEXT, NO NULL): Texto del mensaje (usuario o bot)

tipo (TEXT, NO NULL): “usuario” o “bot”

3. citas
id (SERIAL, NO NULL): Identificador único de la cita

usuario_id (INT, NO NULL): FK → usuarios.id

fecha_inicio (TIMESTAMP, NO NULL): Fecha y hora de inicio del evento

fecha_fin (TIMESTAMP, NO NULL): Fecha y hora de fin del evento

servicio_id (INT, NULL): FK → servicios.id (opcional)

servicio_nombre (TEXT, NO NULL): Nombre o descripción del evento

duracion_minutos (INT, NO NULL): Duración en minutos

precio (NUMERIC, NO NULL): Precio asociado (ej. 0.00)

estado (TEXT, NO NULL): “pendiente”, “confirmada” o “cancelada”

4. historial_citas
id (SERIAL, NO NULL): Identificador único del registro

cita_id (INT, NO NULL): FK → citas.id

cambio (TEXT, NO NULL): Descripción del cambio realizado

datos_previos (JSONB, NULL): Valores anteriores de los campos modificados

fecha_hora (TIMESTAMP, NO NULL): Marca temporal del cambio

5. servicios
id (SERIAL, NO NULL): Identificador único del servicio

nombre (TEXT, NO NULL): Nombre del servicio (p.ej., “Dentista”)

descripcion (TEXT, NULL): Descripción detallada del servicio

activo (BOOLEAN, NO NULL): Disponibilidad del servicio (True/False)

6. mensajes_sistema
id (SERIAL, NO NULL): Identificador único de la plantilla

clave (TEXT, NO NULL): Llave única para identificar el mensaje (p.ej., “pedir_titulo”)

texto (TEXT, NO NULL): Contenido del mensaje con placeholders opcionales

7. integraciones
id (SERIAL, NO NULL): Identificador único de la configuración

nombre (TEXT, NO NULL): Nombre de la integración (p.ej., “GoogleCalendar”)

config_json (JSONB, NO NULL): Parámetros de conexión (claves, URIs, tokens)

activo (BOOLEAN, NO NULL): Estado de la integración (True/False)

8. automatizaciones
id (SERIAL, NO NULL): Identificador único de la tarea

nombre (TEXT, NO NULL): Nombre de la tarea (p.ej., “RecordatorioPrevio”)

cron_expr (TEXT, NO NULL): Expresión cron para programar la ejecución

datos (JSONB, NULL): Payload o parámetros de la ejecución

habilitada (BOOLEAN, NO NULL): Activa o desactiva la automatización

9. logs
id (SERIAL, NO NULL): Identificador único del log

nivel (TEXT, NO NULL): Nivel de log (“INFO”, “WARNING”, “ERROR”)

mensaje (TEXT, NO NULL): Descripción del suceso o error

contexto (JSONB, NULL): Datos adicionales para diagnóstico

timestamp (TIMESTAMP, NO NULL): Marca temporal del registro

## dia 7
## 📝 Actualización de Hoy – Punto Actual de Desarrollo

**Fecha de implementación:** 7 de Octubre, 2025

### ✔️ Lo que hemos completado hasta hoy

- **Reestructuración de la arquitectura**  
  Se definió un **sistema multiagente** con separación clara de responsabilidades:  
  - **Adapter (scripts/telegram_adapter.py):** gestión exclusiva de I/O con Telegram  
  - **Core (src/core):** NLU, detección de intención y gestión de contexto  
  - **Agentes especializados (src/agents):** cada uno maneja un flujo concreto (agendar, consultar, modificar, cancelar)

- **Creación de carpetas y módulos base**  
  - `src/core/`  
  - `src/agents/base_agent.py`  
  - `src/agents/scheduling/agent.py`  
  - `src/agents/query/`  
  - `src/agents/modify/`  
  - `src/agents/cancel/`  
  - `src/services/`  
  - `scripts/`

- **IntentDetector (src/core/intent_detector.py)**  
  - Detección de intenciones por reglas y patrones (keywords y frases completas)  
  - Cálculo de nivel de confianza para cada intención

- **Máquina de estados mejorada (src/services/state_machine.py)**  
  - Estados: `IDLE`, `ASK_TITLE`, `ASK_DATE`, `ASK_DURATION`, `CONFIRM_EVENT`  
  - Transiciones claras para cada paso del flujo de agendado

- **Agente de Scheduling completo (src/agents/scheduling/agent.py)**  
  - Inicio de flujo (“agendar”)  
  - Captura de título, fecha/hora y duración  
  - Validaciones inteligentes: formatos de hora, duraciones flexibles, solapamientos  
  - Confirmación final y limpieza de contexto

- **Modularización del Telegram Adapter (scripts/telegram_adapter.py)**  
  - Enrutamiento de mensajes al `AgentDispatcher` del Core  
  - Anti-concurrencia por usuario  
  - Logging y métricas integradas

- **Procesamiento flexible e inteligente**  
  - **Fechas y horas:** soporte 24h y 12h (`14:30`, `2:30pm`, `14h30`, `a las 10`)  
  - **Duración:** reconocimiento de múltiples formatos (`30 min`, `1h 15m`, `media hora`, `una hora y media`)  
  - **Personalización:** aprendizaje de duración típica, saludo por nombre, emojis contextuales  
  - **Validaciones:** detección de horas ilógicas, comandos de escape (`cancelar`, `salir`), sugerencias de alternativas

- **Preparación para escalabilidad**  
  - Core desacoplado de adapters y agentes  
  - Interfaces claras para añadir nuevos agentes o canales (WhatsApp, Slack)  
  - Base lista para integrar IA/LLM en el módulo de NLU sin afectar el flujo de agentes

***

**Punto actual – Siguiente paso:**  
Implementar `src/core/user_context.py` para centralizar la gestión de estados, datos temporales y preferencias de usuario, y así completar la base del Core antes de crear `agent_dispatcher.py`. 




## 📝 Actualización de Hoy – Punto Actual de Desarrollo

Fecha de implementación: 8 de Octubre, 2025

🔍 Estado actual del repositorio
Carpeta src/core/
– Vacía: faltan los módulos clave:
  - intent_detector.py
  - user_context.py
  - agent_dispatcher.py

Carpeta src/agents/
– Solo existe el agente de “scheduling” completo.
– Faltan los siguientes submódulos:
  - query/agent.py
  - modify/agent.py
  - cancel/agent.py

Carpeta src/services/
– state_machine.py recién creada, pero aún no integrada con el Core.

Carpeta scripts/
– telegram_adapter.py ya modularizado y funcionando.

Pruebas (tests/)
– Hay tests para QueryAgent, pero aún faltan tests para los nuevos módulos.

📍 Punto actual de desarrollo
Listos para arrancar la implementación del Core.
Primer paso: crear src/core/user_context.py para gestionar estados y datos temporales de usuario.
A continuación, se implementará agent_dispatcher.py y se continuarán poblando los módulos del Core según la arquitectura modular definida.