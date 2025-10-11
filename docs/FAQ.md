# Preguntas Frecuentes (FAQ) – Thea IA 2.0

Aquí encontrarás respuestas a las preguntas más habituales sobre la instalación, uso, agentes, base de datos y desarrollo de Thea IA 2.0.

---

## ❓ ¿Qué es Thea IA 2.0?

Thea IA 2.0 es una plataforma modular de agentes inteligentes orientada al procesamiento conversacional y la automatización de tareas mediante Machine Learning, NLP, integraciones API y servicios externos.

---

## ❓ ¿Para quién está pensado el proyecto?

- Usuarios que necesiten un asistente conversacional personalizado (agenda, notas, recordatorios, consultas).
- Desarrolladores y equipos que quieran ampliar los agentes, integraciones o lógica NLP.
- Empresas que deseen adaptar asistentes inteligentes a canales propios (Telegram, webhooks, APIs).

---

## ❓ ¿En qué lenguaje y tecnologías está hecho?

- Python 3.9+
- FastAPI, SQLAlchemy, Alembic, spaCy, scikit-learn, Docker, PostgreSQL.

---parte 2

---

## ⚙️ Instalación y despliegue

### ❓ ¿Cómo instalo Thea IA 2.0?

1. Clona el repositorio:
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia

text
2. Renombra `.env.example` a `.env` y configura tus credenciales y rutas.
3. Instala dependencias:
pip install -r requirements.txt

text

### ❓ ¿Cómo configuro la base de datos?
- Elige PostgreSQL y ajusta la variable `DATABASE_URL` en `.env`.
- Ejecuta migraciones con Alembic:
alembic upgrade head

text

### ❓ ¿Necesito Docker para ejecutar el proyecto?
- Opcional: puedes usar Docker y `docker-compose` para despliegue replicable y testing.

### ❓ ¿Dónde están los scripts de automatización?
- `/scripts/*` incluye setup, deploy, migrate, lint y entrypoints.

---parte 3

---

## 🕹️ Agentes, FSM y NLP

### ❓ ¿Qué agentes están incluidos por defecto?
- Agenda, notas, scheduler, queries, ayuda, fallback.

### ❓ ¿Cómo funciona el sistema FSM?
- La FSM orquesta el flujo conversacional y maneja los estados (`IDLE`, `LISTENING`, `PROCESSING`, etc.).
- Puedes consultar y modificar estados en core/router.py.

### ❓ ¿Qué modelo ML/NLP usa la plataforma?
- SpaCy, scikit-learn y fastText. Modelos configurables y sustituibles.

### ❓ ¿Cómo añadir un nuevo agente?
- Añade la clase, actualiza diccionario de variables, incluye tests y actualiza README.

### ❓ ¿Por qué recibo bajo confidence en intents?
- Ajusta `ML_CONFIDENCE_THRESHOLD` en .env y revisa entrenamiento del modelo.

---

## ⚠️ Errores comunes y soluciones

### ❓ Error: “DB error” o “no se conecta”
- Verifica `.env`, credenciales y estado del servicio PostgreSQL.

### ❓ Error: “Intent not understood”
- Mejora el set de frases y activos de entrenamiento/intents.

### ❓ Error: “Missing information”
- Asegúrate de rellenar todos los campos requeridos y dar formato correcto a las fechas.

---

¿Te paso parte final: contribución, contacto y ampliación de FAQ?**FAQ.md – Parte 4: Contribución, contacto y ampliación FAQ**

🤝 Contribución y contacto
❓ ¿Cómo contribuyo al proyecto?
Sigue la guía CONTRIBUYENDO.md y crea tu rama sobre el fork.

Haz PR detallado y espera revisión.

❓ ¿Dónde reporto un error o sugiero una mejora?
Abre un Issue en GitHub o contacta al responsable del repositorio.

❓ ¿Cómo ampliar la FAQ?
Si detectas dudas frecuentes nuevas, sugiérelas por PR o Issue, siempre actualizando FAQ.md y README.md.

🚩 Referencias rápidas
Consulta README.md para instalación y arquitectura general.

Consulta DICCIONARIO-VARIABLES.md para entender las variables usadas.

Usa ROADMAP.md y CHANGELOG.md para seguir el avance y cambios.

Esta FAQ se actualiza periódicamente según la experiencia de usuarios y desarrolladores.