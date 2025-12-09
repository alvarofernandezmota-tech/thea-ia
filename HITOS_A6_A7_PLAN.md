# 🚀 PLAN DETALLADO - HITOS A.6 y A.7

**Estado Base:** A.4-A.5 ✅ COMPLETADOS  
**Fecha Inicio:** 09 Diciembre 2025  
**Autor:** Álvaro Fernández Mota  

---

## 📊 VISIÓN GENERAL

```
A.4-A.5 (Ya Completado)
     ✅ Context Manager
     ✅ DateTime Parser  
     ✅ Factory Pattern
     ✅ Multi-turn support
         ⬇️
     A.6 - Intent Detection 🏗️
         ⬇️
     A.7 - Event Agent 📅
```

---

## 📄 HITO A.6: INTENT DETECTION

### Objetivo
**Detectar la intención del usuario (CREATE, UPDATE, DELETE, QUERY) y enrutarla correctamente**

### 💻 Arquivos a Crear

```
src/theaia/agents/agenda_agent/
├── intent_detector.py          (🏗️ NEW)
├── intent_router.py            (🏗️ NEW)
└── tests/
    ├── test_intent_detection.py   (🏗️ NEW)
    └── test_intent_routing.py     (🏗️ NEW)
```

### A.6.1: IntentDetector

**Clase:** `IntentDetector`  
**Ubicación:** `src/theaia/agents/agenda_agent/intent_detector.py`

**Responsabilidades:**
- Detectar intención del usuario (CREATE, UPDATE, DELETE, QUERY)
- Calcular confianza de detección
- Manejar ambigüedades

**Métodos Principal:**

```python
class IntentDetector:
    def __init__(self):
        """Inicializar con patrones de intención"""
        pass
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detectar intención del usuario
        
        Retorna:
        {
            "intent": "create_event",  # create_event, update_event, delete_event, query_events
            "confidence": 0.95,          # 0.0 - 1.0
            "entities": {...}           # Entidades extraídas
        }
        """
        pass
    
    def classify_intent(self, text: str) -> str:
        """Clasificar intención sin confianza"""
        pass
    
    def handle_ambiguity(self, candidates: List[str]) -> str:
        """Manejar múltiples intenciones posibles"""
        pass
```

**Patrones de Detección:**

| Intent | Palabras Clave | Ejemplo |
|--------|---|---|
| `create_event` | agendar, crear, programar, planificar, reunir | "Agendar una reunión mañana" |
| `update_event` | cambiar, modificar, actualizar, posponer | "Cambiar la hora a las 3pm" |
| `delete_event` | eliminar, cancelar, borrar, quitar | "Cancelar la reunión" |
| `query_events` | qué tengo, mostrar, listar, buscar, ver | "Qué reuniones tengo hoy" |

### A.6.2: IntentRouter

**Clase:** `IntentRouter`  
**Ubicación:** `src/theaia/agents/agenda_agent/intent_router.py`

**Responsabilidades:**
- Enrutar intenciones detectadas al handler correcto
- Gestionar flujos condicionales
- Manejar errores de enrutamiento

**Métodos Principales:**

```python
class IntentRouter:
    def __init__(self, context_factory: ContextManagerFactory):
        """Inicializar con factory de contextos"""
        pass
    
    def route(self, user_id: str, intent: str, entities: Dict) -> Dict:
        """
        Enrutar a handler correspondiente
        
        Retorna respuesta del handler
        """
        pass
    
    def route_create_event(self, context: ConversationContext, entities: Dict) -> Dict:
        """Manejar CREATE_EVENT"""
        pass
    
    def route_update_event(self, context: ConversationContext, entities: Dict) -> Dict:
        """Manejar UPDATE_EVENT"""
        pass
    
    def route_delete_event(self, context: ConversationContext, entities: Dict) -> Dict:
        """Manejar DELETE_EVENT"""
        pass
    
    def route_query_events(self, context: ConversationContext, entities: Dict) -> Dict:
        """Manejar QUERY_EVENTS"""
        pass
```

### A.6.3: Tests para A.6

**Archivo:** `test_intent_detection.py`  
**Cantidad:** 8-10 tests

```python
class TestIntentDetection:
    def test_detect_create_event(self)
    def test_detect_update_event(self)
    def test_detect_delete_event(self)
    def test_detect_query_events(self)
    def test_confidence_scoring(self)
    def test_handle_ambiguity(self)
    def test_multilingual_intents(self)  # Opcional
    def test_intent_with_entities(self)

class TestIntentRouting:
    def test_route_to_handler(self)
    def test_route_with_context(self)
    def test_error_handling(self)
```

### 💻 Usar desde A.4-A.5

```python
# Intent Detector NECESITA:
from src.theaia.agents.agenda_agent.context_manager import (
    ConversationContext,
    ContextManagerFactory,
    ExtractedEntities
)

# Ya disponible:
context = context_factory.get_or_create_context(user_id)
context.add_message(
    text=user_input,
    intent=detected_intent,      # <- A.6 define esto
    confidence=0.95,
    entities=extracted_entities
)
```

---

## 📅 HITO A.7: EVENT AGENT

### Objetivo
**Crear, actualizar, eliminar y consultar eventos en la base de datos**

### 💻 Archivos a Crear

```
src/theaia/agents/agenda_agent/
├── event_service.py            (🏗️ NEW)
├── event_validator.py          (🏗️ NEW)
├── event_handler.py            (🏗️ NEW - refactor de handler.py)
└── tests/
    ├── test_event_service.py      (🏗️ NEW)
    ├── test_event_validation.py   (🏗️ NEW)
    └── test_event_crud.py         (🏗️ NEW)
```

### A.7.1: EventService

**Clase:** `EventService`  
**Ubicación:** `src/theaia/agents/agenda_agent/event_service.py`

**Responsabilidades:**
- CRUD de eventos (Create, Read, Update, Delete)
- Persistencia en BD
- Transacciones

**Métodos Principales:**

```python
class EventService:
    def __init__(self, session_factory):
        """Inicializar con factory de sesiones BD"""
        pass
    
    def create_event(self, user_id: str, entities: ExtractedEntities) -> Dict:
        """
        Crear nuevo evento
        
        Retorna: {"event_id": ..., "status": "created", ...}
        """
        pass
    
    def update_event(self, event_id: str, entities: ExtractedEntities) -> Dict:
        """
        Actualizar evento existente
        
        Retorna: {"event_id": ..., "status": "updated", ...}
        """
        pass
    
    def delete_event(self, event_id: str) -> Dict:
        """
        Eliminar evento
        
        Retorna: {"event_id": ..., "status": "deleted", ...}
        """
        pass
    
    def get_events(self, user_id: str, filters: Dict = None) -> List[Dict]:
        """
        Obtener eventos con filtros
        
        Filtros:
        - date_from, date_to
        - participant
        - location
        - keyword
        """
        pass
    
    def get_event(self, event_id: str) -> Dict:
        """Obtener evento por ID"""
        pass
```

### A.7.2: EventValidator

**Clase:** `EventValidator`  
**Ubicación:** `src/theaia/agents/agenda_agent/event_validator.py`

**Responsabilidades:**
- Validar datos de evento
- Detectar conflictos
- Validar restricciones

**Métodos Principales:**

```python
class EventValidator:
    def validate_create(self, entities: ExtractedEntities) -> Tuple[bool, str]:
        """
        Validar datos para CREATE
        
        Retorna: (is_valid, error_message)
        
        Validaciones:
        - Título no vacío
        - Fecha en futuro (recomendado)
        - Hora válida (0-23:59)
        - Participantes válidos
        """
        pass
    
    def validate_update(self, event_id: str, entities: ExtractedEntities) -> Tuple[bool, str]:
        """Validar datos para UPDATE"""
        pass
    
    def check_conflicts(self, user_id: str, date: datetime, time: str) -> List[str]:
        """Detectar conflictos de horario"""
        pass
    
    def validate_participants(self, participants: List[str]) -> bool:
        """Validar que los participantes sean válidos"""
        pass
```

### A.7.3: EventHandler

**Clase:** `EventHandler`  
**Ubicación:** `src/theaia/agents/agenda_agent/event_handler.py`

**Responsabilidades:**
- Orquestar operaciones EVENT (integra Service + Validator + Context)
- Generar respuestas naturales
- Manejar excepciones

**Métodos Principales:**

```python
class EventHandler:
    def __init__(self, service: EventService, validator: EventValidator):
        pass
    
    def handle_create(self, user_id: str, context: ConversationContext) -> str:
        """
        Manejar CREATE_EVENT completo
        
        Flujo:
        1. Validar entities
        2. Crear en BD
        3. Actualizar contexto
        4. Generar respuesta
        """
        pass
    
    def handle_update(self, user_id: str, context: ConversationContext) -> str:
        """Manejar UPDATE_EVENT completo"""
        pass
    
    def handle_delete(self, user_id: str, context: ConversationContext) -> str:
        """Manejar DELETE_EVENT con confirmación"""
        pass
    
    def handle_query(self, user_id: str, context: ConversationContext) -> str:
        """Manejar QUERY_EVENTS con filtros"""
        pass
    
    def format_response(self, action: str, result: Dict) -> str:
        """Formatear respuesta natural al usuario"""
        pass
```

### A.7.4: Tests para A.7

**Archivos:** `test_event_service.py`, `test_event_validation.py`, `test_event_crud.py`  
**Cantidad:** 12-15 tests

```python
class TestEventService:
    def test_create_event()
    def test_update_event()
    def test_delete_event()
    def test_get_event()
    def test_get_events_with_filters()
    def test_transaction_handling()

class TestEventValidator:
    def test_validate_create_success()
    def test_validate_create_missing_fields()
    def test_check_time_conflicts()
    def test_validate_participants()

class TestEventHandler:
    def test_handle_create_complete_flow()
    def test_handle_update_complete_flow()
    def test_handle_delete_with_confirmation()
    def test_handle_query_with_filters()
    def test_response_formatting()
```

### 💻 Usar desde A.4-A.6

```python
# Event Service necesita:
from src.theaia.agents.agenda_agent.context_manager import (
    ConversationContext,
    ExtractedEntities
)
from src.theaia.agents.agenda_agent.datetime_parser import DateTimeParser

# Ya disponible:
datetime_parser.parse_datetime(...)  # Parsing de fechas ✅
context.accumulated_entities          # Entidades acumuladas ✅
context.add_message(...)              # Logging de conversación ✅
```

---

## 🌏 CAPAS DE A.6-A.7

```
La Aplicación:

    User Input
        ⬇️
    [A.6 Intent Detector] <- Detecta CREATE/UPDATE/DELETE/QUERY
        ⬇️
    [A.6 Intent Router]   <- Enruta a handler correcto
        ⬇️
    [A.7 Event Handler]   <- Orquesta operación
        ⬇️
    [A.7 Event Service]   <- CRUD en BD
    [A.7 Event Validator] <- Validaciones
        ⬇️
    [A.4 Context Manager] <- Persiste conversación
    [A.5 DateTime Parser] <- Parsea fechas/horas
        ⬇️
    Natural Language Response
```

---

## ⚠️ INTERDEPENDENCIAS

### A.6 Depende De:
- ✅ A.4: `ConversationContext`, `ContextManagerFactory`, `ExtractedEntities`
- ✅ A.5: Tests de integración como baseline

### A.7 Depende De:
- ✅ A.4: `ConversationContext`, `ExtractedEntities`
- ✅ A.5: DateTimeParser para parsing de fechas
- ✅ A.6: Intent detection para saber qué operación realizar
- 😈 Base de Datos: Schema de eventos debe existir

### A.6 No Depende De A.7
- 😈 A.6 puede detectar intenciones sin BD
- 😈 A.7 implementa la lógica de negocio

---

## 📋 CHECKLIST DE ENTRADA A A.6

```
A.4-A.5 COMPLETADO
✅ 26/26 tests pasados
✅ Context Manager funcional
✅ DateTime Parser funcional
✅ Tests base establecidos

REQUISITOS
✅ Python 3.11+
✅ pytest instalado
✅ Fixtures de A.4-A.5 disponibles
✅ Documentación de A.4-A.5 leída

PREPARACION
✅ Crear directorio tests/
✅ Copiar conftest.py con fixtures
✅ Crear test_intent_detection.py
✅ Crear intent_detector.py
```

---

## 📋 CHECKLIST DE ENTRADA A A.7

```
A.6 COMPLETADO
✅ 8-10 tests de intent detection pasados
✅ Intent Detector funcional
✅ Intent Router funcional
✅ Patrones de detección validados

REQUISITOS
✅ SQLAlchemy configurado
✅ BD schema para eventos creado
✅ Event model en models/
✅ EventRepository en repositories/

PREPARACION
✅ Crear event_service.py
✅ Crear event_validator.py
✅ Crear event_handler.py
✅ Crear tests para cada módulo
```

---

## 💪 Capacidades a Entregar

### A.6 Entrega:
- ✅ Detección de 4 intenciones principales
- ✅ Scoring de confianza
- ✅ Manejo de ambigüedades
- ✅ Enrutamiento inteligente
- ✅ 8-10 tests de integración

### A.7 Entrega:
- ✅ CRUD completo de eventos
- ✅ Validación de datos
- ✅ Detección de conflictos
- ✅ Respuestas naturales
- ✅ 12-15 tests de integración

---

## 🚀 Siguientes Pasos

1. **Hoy:** Leer `HITOS_A4_A5_CIERRE.md` completo ✅
2. **Hoy:** Entender API de A.4-A.5 ✅
3. **Mañana:** Iniciar A.6 - Intent Detection
4. **Después de A.6:** Iniciar A.7 - Event Agent

---

**Estado:** Listo para A.6  
**Fecha de Revisión:** 09 Dic 2025  
**Siguiente Revisión:** Despues de A.6 completado  
