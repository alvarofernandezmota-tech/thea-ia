# FallbackAgent - README

## 📋 Descripción

**FallbackAgent** es el agente de fallback del sistema THEAIA. Maneja mensajes que no pueden ser procesados por otros agentes, proporciona respuestas genéricas y ofrece reorientación al usuario.

---

## 🎯 Responsabilidades

- Capturar intenciones desconocidas
- Proporcionar respuestas genéricas apropiadas
- Sugerir alternativas cuando algo no se entiende
- Mantener experiencia conversacional fluida
- Guiar al usuario de regreso al flujo principal

---

## 🔧 Intenciones Soportadas

["fallback", "ninguno", "desconocido"]

text

**Caso de uso**: Cuando el router no puede determinar intención clara

---

## 📁 Estructura de Archivos

fallback_agent/
├── handler.py # Handler principal
├── fallback_conversation_manager.py # Gestión de conversación
├── fallback-agent-readme.md # Este archivo
├── testing.md # Documentación de testing
├── architecture.md # Documentación de arquitectura
├── model/
│ ├── fallback_fsm.py # Máquina de estados
│ └── init.py
└── tests/
├── test_handler.py # Tests unitarios
├── test_fallback_fsm.py # Tests de FSM
└── init.py

text

---

## 🧪 Testing

### **Estado Actual: ✅ COMPLETO**

### **Unit Tests: 4/4 PASSING ✅**

pytest src/theaia/agents/fallback_agent/tests/ -v

text

**Resultados:**
test_can_handle_valid_intents ✅
test_cannot_handle_other_intents ✅
test_fallback_flow ✅
test_fallback_fsm_flow ✅

text

### **E2E Tests: 11/11 PASSING ✅**

pytest src/theaia/tests/e2e/test_fallback_agent_e2e.py -v

text

**Resultados:**
test_unknown_intent_basic ✅
test_unknown_intent_with_clarification ✅
test_unclear_input ✅
test_suggest_similar_intent ✅
test_suggest_features ✅
test_clarify_user_intent ✅
test_partial_match ✅
test_typo_handling ✅
test_ambiguous_input ✅
test_request_human_help ✅
test_report_issue ✅

text

**Total: 15/15 tests passing ✅**

### **Coverage:**

handler.py: 92% ✅
fallback_conversation_manager: 100% ✅

text

---

## 🚀 Uso

### **Inicialización**

from src.theaia.agents.fallback_agent.handler import FallbackAgent

Crear instancia
agent = FallbackAgent(user_id="user_123")

Verificar si puede manejar intención
can_handle = agent.can_handle("desconocido") # True

Procesar mensaje
context = {
"user_id": "user_123",
"tenant_id": "tenant_456",
"session_id": "session_789",
"state": "initial"
}

response, new_state, updated_context = agent.handle(
user_id="user_123",
message="xyz abc",
context=context
)

text

---

## 📊 Flujo de Conversación

Usuario: "hablame de fisica cuantica"
↓
Router no puede determinar intención
↓
FallbackAgent captura mensaje
↓
Proporciona respuesta genérica
↓
Sugiere alternativas
↓
Estado: completed

text

### **Estados FSM:**

- `initial` - Estado inicial
- `awaiting_clarification` - Esperando clarificación del usuario
- `fallback` - Procesando con fallback
- `completed` - Fallback completado
- `idle` - Esperando nueva interacción

---

## 🔄 Integración con Sistema

### **Registro en AgentRegistry:**

from src.theaia.agents.registry import AgentRegistry

registry = AgentRegistry()
registry.register_agent("fallback", FallbackAgent)

text

### **Uso en Router:**

Si todos los agentes rechazan el mensaje
agent = registry.get_agent("fallback")
response = agent.handle(user_id, message, context)

text

---

## ✅ Funcionalidades Implementadas

- ✅ Captura de intenciones desconocidas
- ✅ Respuestas genéricas apropiadas
- ✅ Sugerencias inteligentes
- ✅ Clarificación de entrada ambigua
- ✅ Manejo de typos y errores
- ✅ FSM completa
- ✅ Tests unitarios completos
- ✅ Tests E2E completos

---

## 📝 Ejemplos de Interacción

### **Entrada Desconocida:**

Usuario: "hablame de fisica cuantica"
THEAIA: "No estoy seguro de entender esa solicitud.
Puedo ayudarte con:
- Crear y gestionar notas
- Organizar eventos y citas
- Configurar recordatorios
- Consultar información
¿Con qué puedo ayudarte?"

text

### **Entrada Ambigua:**

Usuario: "esto aquello"
THEAIA: "Parece que tu solicitud no es clara.
¿Podrías ser más específico? Por ejemplo:
- 'crear nota'
- 'nuevo evento'
- 'recordatorio'
- 'ayuda'"

text

### **Typo o Similitud:**

Usuario: "crer nota"
THEAIA: "¿Quisiste decir 'crear nota'?
O si necesitas otra cosa:
- crear evento
- recordatorio
- buscar información"

text

---

## 🔧 Configuración

### **Sin configuración especial requerida**

FallbackAgent es un agente simple que no requiere:
- ❌ Base de datos
- ❌ APIs externas
- ❌ Configuración compleja

---

## 📊 Métricas

- **Tests**: 15/15 passing ✅
- **Coverage**: 92-100% ✅
- **Estado**: Production-ready ✅
- **Complejidad**: Baja ✅

---

## 🎯 Estado del Agente

| Componente | Estado | Notas |
|-----------|--------|-------|
| Handler | ✅ Completo | Funcional al 100% |
| FSM | ✅ Completo | Estados bien definidos |
| Tests Unitarios | ✅ 4/4 | 100% passing |
| Tests E2E | ✅ 11/11 | 100% passing |
| Documentación | ✅ Completo | README actualizado |
| Producción | ✅ Ready | Listo para deploy |

---

## 🚀 Próximos Pasos

**FallbackAgent está 100% completado. No requiere trabajo adicional.**

---

## 📅 Historial de Cambios

### **2025-11-24**
- ✅ Implementación completa del agente
- ✅ Tests unitarios: 4/4 passing
- ✅ Tests E2E: 11/11 passing
- ✅ Coverage: 92-100%
- ✅ Documentación completa

---

## 👥 Mantenimiento

**Responsable**: Equipo THEAIA  
**Última actualización**: 2025-11-24  
**Estado**: Production-ready ✅