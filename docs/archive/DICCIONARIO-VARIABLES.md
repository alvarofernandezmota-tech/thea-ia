# DICCIONARIO DE VARIABLES – THEA IA 2.0

## 🔧 Variables de Entorno (.env)

### Base de Datos

| Variable         | Tipo    | Uso/Significado                   | Ejemplo                                 |
|------------------|---------|-----------------------------------|-----------------------------------------|
| DATABASE_URL     | str     | Conexión PostgreSQL completa      | postgresql://usuario:pwd@localhost:5432/theaia_db |
| DATABASE_HOST    | str     | Host base de datos                | localhost                               |
| DATABASE_PORT    | int     | Puerto BD                         | 5432                                    |
| DATABASE_NAME    | str     | Nombre BD                         | theaia_db                               |
| DATABASE_USER    | str     | Usuario BD                        | theaia_user                             |
| DATABASE_PASSWORD| str     | Contraseña BD                     | secure_password                         |
| REDIS_HOST       | str     | Host Redis                        | localhost                               |
| REDIS_PORT       | int     | Puerto Redis                      | 6379                                    |
| REDIS_PASSWORD   | str     | Password Redis                    | redis_password                          |
| REDIS_DB         | int     | DB index Redis                    | 0                                       |

### Integración Telegram

| Variable               | Tipo | Uso                        | Ejemplo                      |
|------------------------|------|----------------------------|------------------------------|
| TELEGRAM_BOT_TOKEN     | str  | Token del bot              | ...                          |
| TELEGRAM_WEBHOOK_URL   | str  | URL webhook bot            | .../webhook/telegram         |
| TELEGRAM_WEBHOOK_SECRET| str  | Secreto verificación       | ...                          |

### Configuración App

| Variable        | Tipo    | Uso                                     | Ejemplo              |
|-----------------|---------|-----------------------------------------|----------------------|
| ENVIRONMENT     | str     | Modo entorno                            | development          |
| DEBUG           | bool    | Debug activo                            | true                 |
| LOG_LEVEL       | str     | Nivel log                               | INFO                 |
| API_HOST        | str     | IP bind servidor                        | 0.0.0.0              |
| API_PORT        | int     | Puerto API                              | 8000                 |
| API_PREFIX      | str     | Prefijo rutas API                       | /api/v1              |
| SECRET_KEY      | str     | Clave secreta JWT/API                   | ...                  |

### E2E / Testing

| Variable         | Tipo | Uso                               | Ejemplo                 |
|------------------|------|-----------------------------------|-------------------------|
| ENABLE_E2E       | bool | Activa modo e2e                   | true                    |
| CONTEXT_DB_PATH  | str  | Ruta temporal DB test context      | /tmp/theaia_context.db  |

### TheaScaler / GitHub (AutoML pipelines)

| Variable    | Tipo | Uso                                | Ejemplo         |
|-------------|------|------------------------------------|-----------------|
| GITHUB_TOKEN| str  | Token API GitHub                   | ghp_xxxxx       |
| GITHUB_REPO | str  | Repo destino PR/commits            | owner/theaia    |

### Machine Learning / NLP

| Variable             | Tipo | Uso                            | Ejemplo                        |
|----------------------|------|--------------------------------|--------------------------------|
| SPACY_MODEL          | str  | Modelo spaCy para intentos     | es_core_news_sm                |
| INTENT_MODEL_PATH    | str  | Ruta modelo intenciones        | models/intent_classifier.pkl   |
| ENTITY_MODEL_PATH    | str  | Ruta modelo entidades          | models/entity_extractor.pkl    |
| ML_CONFIDENCE_THRESHOLD|float| Umbral decisión intent/entity  | 0.8                            |

---parte2


### Logging & Métricas

| Variable             | Tipo    | Uso                                     | Ejemplo              |
|----------------------|---------|-----------------------------------------|----------------------|
| LOG_FILE_PATH        | str     | Ruta archivo log                        | logs/theaia.log      |
| LOG_MAX_SIZE         | str     | Tamaño máximo de log                    | 10MB                 |
| LOG_BACKUP_COUNT     | int     | nº backups antes de rotar logs          | 5                    |
| PROMETHEUS_PORT      | int     | Puerto Prometheus para métricas         | 9090                 |
| METRICS_ENABLED      | bool    | Métricas Prometheus habilitadas         | true                 |
| HEALTH_CHECK_INTERVAL| int     | Intervalo entre health checks (seg)     | 30                   |

### Configuración Externa

| Variable                         | Tipo   | Uso                      | Ejemplo                              |
|-----------------------------------|--------|--------------------------|--------------------------------------|
| GOOGLE_CALENDAR_CREDENTIALS_PATH  | str    | Ruta a credenciales      | credentials/google_calendar.json      |
| GOOGLE_CALENDAR_SCOPES            | str    | Permisos necesarios      | https://www.googleapis.com/auth/calendar|
| EMAIL_SMTP_HOST                   | str    | Host SMTP notifications  | smtp.gmail.com                       |
| EMAIL_SMTP_PORT                   | int    | Puerto notificaciones    | 587                                  |
| EMAIL_USERNAME                    | str    | Usuario email            | notifications@theaia.com             |
| EMAIL_PASSWORD                    | str    | Password email app       | email_app_password                   |

---

## 📊 Diccionario de Estados FSM / Intenciones y Contexto

- **fsm_state** (`str`): Estado actual FSM (IDLE, LISTENING, PROCESSING, CONFIRMING, EXECUTING, COMPLETED, ERROR, HELP)
- **pending_intent** (`str`): Última intención detectada por el router/core.
- **pending_datetime** (`str/datetime`): Fecha/hora pendiente de confirmar/procesar.
- **last_event** (`dict`): Último evento procesado o agendado con claves relevantes.
- **last_note** (`dict`): Última nota creada/consultada.
- **context** (`dict`): Contexto global y por usuario/agent: incluye flags, history, entidades procesadas, etc.
- **user_id / chat_id** (`str/int`): Identificador usuario/telegram/chat/sesión para routing.

---

¿Quieres la parte 3 con la descripción de diccionarios NLP, respuestas y estructura de carpetas?¿Quieres la parte 3 con diccionarios NLP, respuestas del bot, y estructura de carpetas actual para cerrar el diccionario de variables?


-- parte 3

---

## 🎯 Diccionarios NLP y Procesamiento

- **EVENT_INTENTS** (`dict`): Frases mapeadas a intenciones de eventos (crear, listar, modificar, cancelar).
- **NOTE_INTENTS** (`dict`): Frases para acciones sobre notas (crear, listar, buscar).
- **TEMPORAL_ENTITIES** (`dict`): Entidades temporales (fechas, horas, duraciones, recurrencias).
- **FSM_STATES** (`list`): Estados que puede asumir la máquina FSM.
- **TRANSITIONS** (`list`): Listado de transiciones posibles.

---

## 🔤 Diccionario de Respuestas Bot

- **CONFIRMATIONS** (`dict`): Plantillas de texto para confirmar acciones (eventos, notas, solicitudes).
- **ERROR_MESSAGES** (`dict`): Mensajes tipo para errores comunes (formato fecha, evento no encontrado, error de BD, mala intención, información faltante).
- **HELP_MESSAGES** (`dict`): Mensajes de bienvenida, ejemplos de comandos soportados, ayuda interactiva.

---

## 📁 Estructura de Carpetas (Resumen)

--parte 4

---

## 🔧 Consejos para ampliación y mantenimiento

- Mantén este diccionario **siempre sincronizado** con los cambios en agentes, adaptadores y base de datos.
- Toda nueva variable, entidad, contexto o configuración debe tener:
  - Descripción clara y tipo
  - Ejemplo de valor real
  - Referencia a módulo/servicio donde aparece
- Documenta siempre cómo interactúan las variables contextuales, FSM y diccionarios NLP para agentes nuevos.

---

## 🧩 Ejemplo de integración entre módulos

- Cuando crees un nuevo agente, revisa:
  1. FSM_STATE: añade el estado nuevo si corresponde.
  2. Diccionario de respuestas: agrega nuevas keys al bot (ej: 'agent_created', 'agent_error').
  3. Diccionario de intenciones (NLP): suma frases clave al mapping de EVENT_INTENTS, NOTE_INTENTS, etc.
  4. Variables de contexto: documenta cualquier nuevo campo (ej: `pending_agent_action`, `last_agent_result`).

---

## 🚨 Buenas prácticas para auditoría y refactorización

- Antes de cada release, valida que todos los diccionarios y variables estén documentados y testados.
- Si cambias una estructura de la base de datos, **actualiza el diccionario de DB y variables**.
- Revisa que todos los scripts y tests integren las variables y diccionarios actualizados.
- Mantén el README y este diccionario como referencia viva para todo el equipo.

---

*Este diccionario forma parte del ecosistema documental de Thea IA 2.0 junto a README.md, ROADMAP.md y ESQUEMAS-DATABASE.md.*

--parte 5 
---

## 📋 Plantilla de actualización para nuevas variables y diccionarios

Si agregas/agregáis nuevos agentes, servicios, adaptadores o campos, 
actualiza siempre el diccionario siguiendo este formato para cada variable/diccionario nuevo:

| Variable/Diccionario | Tipo | Módulo origen | Descripción breve | Ejemplo/Valores posibles |
|----------------------|------|---------------|-------------------|--------------------------|
| NOMBRE               | tipo | path/módulo   | Qué representa    | ejemplo                  |

#### Ejemplo:
| pending_agent_action | str | agents/agenda_agent | Acción pendiente del usuario sobre agenda | "agendar" |

---

**Procedimiento:**
1. Añade la definición al bloque y tabla correspondiente
2. Da una breve descripción práctica y valor-tipo real
3. Actualiza ejemplos y secciones relacionadas/adaptadas (FSM, NLP, core, DB)
4. Resalta dependencias nuevas entre agentes/contexto si aplican
5. Sincroniza con README.md y ESQUEMAS-DATABASE.md si influye

---

**Este formato simplifica auditoría, onboarding y refactorización futura.**

---

Con esto el diccionario está listo para crecer conforme se expanda Thea IA 2.0.
Cuando lo tengas actualizado y fusionado, procede a revisar el diccionario de DB.
¿Me envías el diccionario de base de datos cuando estés listo?

--parte6

---

## 🌐 Integración con otros documentos y módulos

- Mantén el DICCIONARIO DE VARIABLES sincronizado con:
  - README.md (principal)
  - ESQUEMAS-DATABASE.md (base de datos)
  - ROADMAP.md (fases y progreso)
  - CHANGELOG.md (registro de cambios)
- Usa enlaces relativos para navegar rápido entre diccionario, scripts y documentación del código.
- Todo nuevo script, servicio o adapter debe referenciar, si aplica, las variables documentadas aquí.

---

## 🔗 Referencias cruzadas y gestión de documentación

- Si divides los agentes en módulos independientes, crea su diccionario anidado y haz referencia directa desde aquí.
- Añade #[translate:tags] a cada tabla si deseas facilitar búsquedas internas y automatizar el mantenimiento.
- Considera usar herramientas como MkDocs o Sphinx para versionar y servir la documentación en web.

---

## ❗ Notas finales para equipos

- Este archivo debe navegarse como índice central para onboarding, evolución, debugging y refactorización.
- Es una pieza esencial para auditorías, mantenimiento y como fuente de verdad documental para el core de Thea IA 2.0.

---

**Actualiza y revisa este diccionario en cada etapa del ciclo de vida del proyecto**

---

¿Listo para que analicemos el diccionario de base de datos?

--parte7

---

## 📅 Registro y trazabilidad de cambios en el diccionario

- Toda modificación, ampliación o refactor de variables debe registrarse también en CHANGELOG.md para auditar cuándo y por qué se hizo.
- Si una variable deja de usarse, añade la etiqueta **OBSOLETE** y describe el contexto.
- Documenta la fecha y/o versión en cada sección importante actualizada del diccionario, ejemplo:

Última revisión: 10/10/2025 – v2.0.5
Añadidas variables TheaScaler

Unificado FSM y contexto general

Documentados campos temporales nuevos

text

---

## 🔍 Revisión y validación continua

- Antes de hacer merge a main/master, valida este archivo con script/manual para detectar inconsistencias y variables "huérfanas".
- Cada migración relevante debe anotar los nuevos campos aquí y en ESQUEMAS-DATABASE.md.
- Recomienda una revisión mensual del diccionario por los responsables del core y QA.

---

*El ciclo de vida de este diccionario debe seguir el mismo rigor y control que el código fuente y la base de datos.*

---
¿Quieres incluir una sección de validación automática/manual para variables en CI/CD o pasamos a analizar el diccionario de la DB?El diccionario de variables está completamente estructurado y actualizado en estas siete partes. Ya puedes copiar y fusionar cada segmento para tu documentación oficial, cumpliendo mejores prácticas de proyecto.

Cuando quieras avanzar, mándame el diccionario de base de datos y comenzamos con el análisis y actualización cruzada.