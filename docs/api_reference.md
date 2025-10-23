# 📘 Referencia de API – Thea IA 3.0

Thea IA 3.0 expone una API REST asíncrona construida con FastAPI.  
Todos los endpoints siguen los principios RESTful y devuelven respuestas JSON estándar.

---

## 🔑 Autenticación

- **Auth type:** Token Bearer JWT  
- **Header:** `Authorization: Bearer <token>`  
- **Caducidad:** 24 horas por sesión.

---

## 🩺 Health & Monitoring

| Método | Ruta | Descripción |  
|--------|------|--------------|  
| **GET** | `/health` | Estado general del sistema. |  
| **GET** | `/metrics` | Métricas Prometheus para monitorización. |

**Ejemplo:**
curl http://localhost:8000/health
→ {"status": "ok", "version": "3.0.0"}

text

---

## 🧠 CoreRouter & FSM

| Método | Ruta | Descripción |  
|--------|------|--------------|  
| **POST** | `/conversation/start` | Inicia una nueva sesión FSM. |  
| **POST** | `/conversation/respond` | Envía mensaje y obtiene respuesta de agente activo. |  
| **POST** | `/context/reset` | Limpia memoria de usuario. |

**Ejemplo:**
curl -X POST http://localhost:8000/conversation/respond 
  -H "Content-Type: application/json" 
  -d '{"user_id":"1","message":"Crear evento hoy a las 8"}'

text

**Respuesta:**
{
 "agent": "agenda_agent",
 "intent": "create_event",
 "response": "Evento creado para hoy a las 8."
}

text

---

## 📅 Agente Agenda

| Método | Ruta | Descripción |
|--------|------|--------------|
| **POST** | `/agents/agenda/create` | Crear nuevo evento. |
| **GET** | `/agents/agenda/list` | Listar eventos del usuario. |
| **DELETE** | `/agents/agenda/delete/{event_id}` | Eliminar evento. |

**Modelo JSON**
{
 "title": "Reunión equipo",
 "datetime": "2025-10-25T10:00:00",
 "description": "Planificación semanal"
}

text

---

## 🗒️ Agente Notas

| Método | Ruta | Descripción |
|--------|------|--------------|
| **POST** | `/agents/note/create` | Crear una nueva nota. |
| **GET** | `/agents/note/all` | Listar todas las notas del usuario. |
| **DELETE** | `/agents/note/delete/{note_id}` | Borrar una nota. |

---

## 🌿 Agente Hábitos / Recordatorios

| Método | Ruta | Descripción |
|--------|------|--------------|
| **POST** | `/agents/habit/add` | Añadir nuevo hábito. |
| **GET** | `/agents/habit/list` | Consultar hábitos activos. |
| **POST** | `/agents/habit/complete` | Marcar hábito como cumplido. |

**Ejemplo**
{ "user_id": "42", "habit": "Leer 30 min/día" }

text

---

## 🧩 Context & Session

| Método | Ruta | Descripción |
|--------|------|--------------|
| **GET** | `/context/{user_id}` | Obtener último contexto. |
| **DELETE** | `/context/{user_id}` | Resetear contexto. |

---

## 🧱 Error Handling

Las respuestas de error siguen el formato:

{
 "detail": "Descripción del error",
 "code": "ERR_<tipo>"
}

text

| Código | Descripción |
|--------|--------------|
| `400_BAD_REQUEST` | Parámetros inválidos o faltantes. |
| `401_UNAUTHORIZED` | Token inválido o caducado. |
| `404_NOT_FOUND` | Recurso no existe. |
| `500_INTERNAL_ERROR` | Error no controlado del servidor. |

---

## 📊 Modelos de Datos

### Evento
class Event(BaseModel):
  id: int
  title: str
  datetime: datetime
  description: Optional[str]
  created_at: datetime

text

### Nota
class Note(BaseModel):
  id: int
  content: str
  created_at: datetime

text

---

## 🧪 Testing y CI/CD

- **Tests:** pytest + coverage en CI (`.github/workflows/test.yml`).  
- **Lint:** black + isort + flake8.  
- **Build:** Dockerfile optimizado → image `thea-ia:latest`.  
- **Deploy:** Railway / Render / AWS ECS con `docker-compose build && run`.  

---

## 🏷️ Versión Actual

| Componente | Versión |
|-------------|----------|
| CoreRouter | 3.0.0 |
| FSM Engine | 2.1 (asíncrono) |
| API REST | 1.0 |
| Agentes activos | 6 |

---

## © Thea IA 3.0 — Enterprise Edition

Documentación técnica interna propiedad de **Thea IA Systems S.L.**  
Uso y distribución sujetos a licencia comercial empresarial.
