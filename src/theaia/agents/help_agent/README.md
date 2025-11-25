# HelpAgent - README

## 📋 Descripción

**HelpAgent** es el agente de ayuda del sistema THEAIA. Proporciona información sobre las capacidades del asistente, comandos disponibles y guía al usuario sobre cómo interactuar con el sistema.

---

## 🎯 Responsabilidades

- Responder preguntas sobre funcionalidades del sistema
- Listar comandos disponibles
- Explicar capacidades de cada agente
- Guiar al usuario en el uso de THEAIA
- Proporcionar ejemplos de uso

---

## 🔧 Intenciones Soportadas

["ayuda", "help", "comando", "comandos", "qué puedes hacer", "capacidades"]

text

---

## 📁 Estructura de Archivos

help_agent/
├── handler.py # Handler principal del agente
├── help_conversation_manager.py # Gestión de conversación
├── help-agent-readme.md # Este archivo
├── model/
│ ├── help_fsm.py # Máquina de estados
│ └── init.py
└── tests/
├── test_handler.py # Tests unitarios del handler
├── test_help_fsm.py # Tests de la FSM
└── init.py

text

---

## 🧪 Testing

### **Estado Actual: ✅ COMPLETO**

### **Unit Tests: 4/4 PASSING ✅**

pytest src/theaia/agents/help_agent/tests/ -v

text

**Resultados:**
test_can_handle_help_intents ✅
test_cannot_handle_other_intents ✅
test_help_flow ✅
test_help_fsm_flow ✅

text

### **E2E Tests: 14/14 PASSING ✅**

pytest src/theaia/tests/e2e/test_help_agent_e2e.py -v

text

**Resultados:**
test_help_basic ✅
test_help_commands ✅
test_help_features ✅
test_help_capabilities ✅
test_help_agents ✅
test_help_note_agent ✅
test_help_event_agent ✅
test_help_agenda_agent ✅
test_help_query_agent ✅
test_help_reminder_agent ✅
test_help_scheduler_agent ✅
test_help_fallback_agent ✅
test_help_specific_command ✅
test_help_examples ✅

text

**Total: 18/18 tests passing ✅**

### **Coverage:**

handler.py: 100% ✅
help_conversation_manager: 100% ✅

text

---

## 🚀 Uso

### **Inicialización**

from src.theaia.agents.help_agent.handler import HelpAgent

Crear instancia
agent = HelpAgent(user_id="user_123")

Verificar si puede manejar intención
can_handle = agent.can_handle("ayuda") # True

Procesar mensaje
context = {
"user_id": "user_123",
"tenant_id": "tenant_456",
"session_id": "session_789",
"state": "initial"
}

response, new_state, updated_context = agent.handle(
user_id="user_123",
message="ayuda",
context=context
)

text

---

## 📊 Flujo de Conversación

Usuario: "ayuda"
↓
HelpAgent detecta intención
↓
Muestra información de ayuda
↓
Estado: completed

text

### **Estados FSM:**

- `initial` - Estado inicial
- `providing_help` - Proporcionando información de ayuda
- `completed` - Ayuda proporcionada
- `idle` - Esperando nueva interacción

---

## 🔄 Integración con Sistema

### **Registro en AgentRegistry:**

from src.theaia.agents.registry import AgentRegistry

registry = AgentRegistry()
registry.register_agent("help", HelpAgent)

text

### **Detección de Intención:**

El router del sistema detecta intenciones de ayuda y delega a HelpAgent automáticamente.

---

## ✅ Funcionalidades Implementadas

- ✅ Respuestas de ayuda general
- ✅ Lista de comandos disponibles
- ✅ Explicación de capacidades por agente
- ✅ Ejemplos de uso
- ✅ Guía de navegación del sistema
- ✅ FSM completa para gestión de conversación
- ✅ Tests unitarios completos
- ✅ Tests E2E completos

---

## 📝 Ejemplos de Interacción

### **Ayuda General:**

Usuario: "ayuda"
THEAIA: "¡Hola! Soy THEAIA, tu asistente personal. Puedo ayudarte con:
- Gestión de notas
- Organización de eventos
- Recordatorios
- Consultas de información
¿En qué puedo ayudarte?"

text

### **Comandos Disponibles:**

Usuario: "¿qué comandos hay?"
THEAIA: "Comandos disponibles:
- crear nota: Crear una nueva nota
- listar notas: Ver todas tus notas
- crear evento: Añadir evento al calendario
- recordar: Crear un recordatorio
- buscar: Consultar información"

text

### **Capacidades de Agente:**

Usuario: "¿qué puede hacer el agente de notas?"
THEAIA: "El NoteAgent puede:
- Crear notas de texto
- Listar tus notas
- Buscar notas por contenido
- Actualizar notas existentes
- Eliminar notas"

text

---

## 🔧 Configuración

### **Sin configuración especial requerida**

HelpAgent es un agente simple que no requiere:
- ❌ Base de datos
- ❌ APIs externas
- ❌ Configuración compleja

---

## 📊 Métricas

- **Tests**: 18/18 passing ✅
- **Coverage**: 100% ✅
- **Estado**: Production-ready ✅
- **Complejidad**: Baja ✅

---

## 🎯 Estado del Agente

| Componente | Estado | Notas |
|-----------|--------|-------|
| Handler | ✅ Completo | Funcional al 100% |
| FSM | ✅ Completo | Estados bien definidos |
| Tests Unitarios | ✅ 4/4 | 100% passing |
| Tests E2E | ✅ 14/14 | 100% passing |
| Documentación | ✅ Completo | README actualizado |
| Producción | ✅ Ready | Listo para deploy |

---

## 🚀 Próximos Pasos

**HelpAgent está 100% completado. No requiere trabajo adicional.**

Posibles mejoras futuras (opcionales):
- Añadir ayuda contextual basada en historial
- Integrar tutoriales interactivos
- Añadir sugerencias inteligentes

---

## 📅 Historial de Cambios

### **2025-11-24**
- ✅ Implementación completa del agente
- ✅ Tests unitarios: 4/4 passing
- ✅ Tests E2E: 14/14 passing
- ✅ Coverage: 100%
- ✅ Documentación completa

---

## 👥 Mantenimiento

**Responsable**: Equipo THEAIA  
**Última actualización**: 2025-11-24  
**Estado**: Production-ready ✅