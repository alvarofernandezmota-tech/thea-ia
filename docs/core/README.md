# Core - Sistema Central de THEA IA

**Version:** v3.0.0
**Status:** ✅ Production Ready
**Calificación Auditoría:** 8.8/10 - MUY BUENO
**Last Updated:** 06 Enero 2026

## 📋 Índice

- [Visión General](#visión-general)
- [Componentes](#componentes)
- [Documentación](#documentación)
- [Métricas](#métricas)

---

## 🎯 Visión General

El módulo **`core/`** es el corazón del sistema THEA IA. Contiene:

- **FSM (Finite State Machine):** Motor de estados conversacional
- **Conversation Manager:** Orquestación de diálogos
- **Multi-Agent System:** Coordinación entre agentes
- **Context Management:** Gestión de contexto
- **Lifecycle Management:** Gestión del ciclo de vida

### Ubicación
```
src/theaia/core/
├── agents/              # Sistema de agentes (movido recientemente)
├── conversation/        # Gestión conversacional
├── fsm/                 # Finite State Machine
├── multi_agent/         # Coordinación multi-agente
└── __init__.py
```

---

## 🏗️ Componentes Principales

### 1. FSM (Finite State Machine)
- **Calificación:** 9.0/10 ⭐
- **Tests:** 196 tests | 90%+ coverage
- **LOC:** ~3,500

### 2. Conversation Manager
- **Calificación:** 8.8/10
- **Tests:** 56 tests | 85% coverage
- **LOC:** ~2,000

### 3. Multi-Agent System
- **Calificación:** 8.7/10
- **Tests:** 67 tests | 87% coverage
- **LOC:** ~1,500

### 4. Lifecycle Management
- **Calificación:** 9.2/10 ⭐ EXCELENTE
- **Tests:** Thread-safe singleton
- **LOC:** ~1,000

---

## 📊 Métricas del Core

| Métrica | Valor |
|---------|-------|
| **Total Archivos** | ~60 |
| **Total LOC** | ~8,000 |
| **Tests** | 370+ |
| **Coverage** | 88% promedio |
| **Complejidad** | Alta |

---

## 📚 Documentación Detallada

### Por Componente

- 📖 **FSM:** [fsm.md](./fsm.md) - Finite State Machine
- 📖 **Conversation:** [conversation.md](./conversation.md) - Conversation Manager
- 📖 **Multi-Agent:** [multi-agent.md](./multi-agent.md) - Sistema multi-agente
- 📖 **Context:** [context.md](./context.md) - Context Management
- 📖 **Lifecycle:** [lifecycle.md](./lifecycle.md) - Lifecycle Manager

### Documentación Relacionada

- 📖 [Agents](../agents/overview.md) - 7 agentes especializados
- 📖 [Architecture](../architecture/overview.md) - Arquitectura general
- 📖 [API](../api/README.md) - API endpoints
- 📖 [Database](../database/README.md) - Schema y modelos

---

## 🎖️ Resultado Auditoría

### Fortalezas
- ✅ Arquitectura modular excelente
- ✅ FSM avanzada (percentil 90+)
- ✅ Alta cobertura de tests
- ✅ Patrones de diseño bien aplicados

### Áreas de Mejora
- ⚠️ Algunos módulos 3 meses sin actualizar
- ⚠️ Documentación de onboarding necesaria
- ⚠️ Complejidad alta (curva de aprendizaje)

---

## 🚀 Quick Start

```python
from theaia.core.fsm import StateMachine
from theaia.core.conversation import ConversationManager
from theaia.core.multi_agent import AgentCoordinator

# Inicializar componentes
fsm = StateMachine()
conversation = ConversationManager()
coordinator = AgentCoordinator()
```

---

**Fuente:** Auditoría Diciembre 2025 - [03_audit_src](../audit/audit_diciembre_2025/03_audit_src/)
**Mantenido por:** Álvaro Fernández Mota
**Estado:** ✅ Production Ready
