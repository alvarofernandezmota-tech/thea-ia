# 🎓 Agent Best Practices — THEA IA

**Version:** 2.0  
**Last Updated:** 06 January 2026  
**Status:** ✅ Active  
**Maintained by:** Agents Team

---

## 🎯 Fundamental Principles

### 1️⃣ Single Responsibility Principle

Each agent does **ONE thing** and does it well.

✅ GOOD:

AgendaAgent: ONLY manages appointments

NoteAgent: ONLY manages notes

QueryAgent: ONLY searches (read-only)

ReminderAgent: ONLY manages standalone reminders

❌ BAD:

AgendaAgent that also handles notes

QueryAgent that modifies data

One "SuperAgent" doing everything

text

### 2️⃣ Agent Isolation

Agents **NEVER** communicate directly with each other.

❌ BAD: AgentA → AgentB (direct call)
✅ GOOD: AgentA → Orchestrator → AgentB

The Orchestrator is the ONLY coordinator.

text

### 3️⃣ Read vs Write Separation

Clear distinction between read-only and write agents.

WRITE Agents (CRUD):

AgendaAgent: Create/update/delete appointments

NoteAgent: Create/update/delete notes

ReminderAgent: Create/update/delete reminders

READ Agent (Search):

QueryAgent: Search-only, NO modifications

text

### 4️⃣ Idempotency

Same input = Same output (when possible).

```python
# Idempotent: Creating appointment with same ID
create_appointment(id=123, date="2026-01-07")
  → First call: Creates appointment
  → Second call: Returns existing (no duplicate)

# Non-idempotent is acceptable for:
- Searches (results may change over time)
- List operations (data changes)
5️⃣ Robust Error Handling
Never fail silently. Always return structured errors.

python
# Good error response
{
  "success": False,
  "error": {
    "code": "CONFLICT",
    "message": "Appointment conflicts with existing booking",
    "details": {
      "existing_appointment": "appt_456",
      "conflict_time": "15:00"
    }
  }
}
🔄 Orchestrator Patterns
Pattern 1: Intent Routing
The Orchestrator classifies intents and routes to agents.

python
class Orchestrator:
    def route_message(self, message):
        intent = self.classify_intent(message)
        
        # Route to appropriate agent
        if intent == "BOOK_APPOINTMENT":
            return self.agenda_agent.handle(message)
        elif intent == "SEARCH":
            return self.query_agent.handle(message)
        elif intent == "CREATE_NOTE":
            return self.note_agent.handle(message)
        elif intent == "SET_REMINDER":
            return self.reminder_agent.handle(message)
        else:
            # Fallback handled by Orchestrator
            return self.handle_unknown_intent(message)
Pattern 2: Fallback Handling
Fallback is NOT an agent - it's an Orchestrator responsibility.

python
class Orchestrator:
    def handle_unknown_intent(self, message):
        """Handles unrecognized user input"""
        return {
            "response": "No entendí tu solicitud. ¿Podrías reformularla?",
            "suggestions": [
                "Agendar una cita",
                "Buscar información",
                "Crear una nota",
                "Configurar un recordatorio"
            ],
            "help_available": True
        }
❌ DON'T: Create a FallbackAgent
✅ DO: Implement orchestrator.handle_unknown_intent()

Pattern 3: Help System
Each agent exposes its help, Orchestrator aggregates.

python
# Each agent implements
class AgendaAgent:
    def get_help(self):
        return {
            "name": "AgendaAgent",
            "description": "Gestiona citas y calendario",
            "commands": [
                {"example": "Agendar cita mañana 3pm", "intent": "BOOK"},
                {"example": "Ver disponibilidad viernes", "intent": "CHECK"},
                {"example": "Cancelar cita", "intent": "CANCEL"}
            ],
            "keywords": ["cita", "agendar", "calendario", "disponibilidad"]
        }

# Orchestrator aggregates
class Orchestrator:
    def get_global_help(self):
        return {
            "agents": [
                self.agenda_agent.get_help(),
                self.query_agent.get_help(),
                self.note_agent.get_help(),
                self.reminder_agent.get_help()
            ],
            "general_commands": [
                "/help - Ver esta ayuda",
                "/status - Ver estado del sistema"
            ]
        }
❌ DON'T: Create a HelpAgent
✅ DO: Implement agent.get_help() in each agent

🏗️ Agent Structure
Recommended File Structure
text
src/theaia/agents/<agent_name>/
├── agent.py              # Main agent class
├── handler.py            # Command handler (if needed)
├── services/             # Business logic
│   ├── service_a.py
│   └── service_b.py
├── models/               # Data models
├── schemas/              # Pydantic schemas
├── tests/                # Test suite
│   ├── test_agent.py
│   ├── test_services.py
│   └── test_integration.py
└── tools/                # Utilities
Agent Class Template
python
from typing import Dict, Any, Optional

class AgentTemplate:
    """Agent description"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = "AgentName"
        self.version = "1.0"
    
    def handle(self, message: str, context: Dict) -> Dict[str, Any]:
        """Main entry point"""
        try:
            # 1. Validate input
            self._validate_input(message, context)
            
            # 2. Process request
            result = self._process(message, context)
            
            # 3. Return success
            return {
                "success": True,
                "data": result,
                "agent": self.name
            }
        except Exception as e:
            # 4. Return structured error
            return self._handle_error(e)
    
    def get_help(self) -> Dict[str, Any]:
        """Return agent help information"""
        return {
            "name": self.name,
            "description": "What this agent does",
            "commands": [],
            "keywords": []
        }
    
    def _validate_input(self, message: str, context: Dict):
        """Validate and sanitize input"""
        if not message:
            raise ValueError("Empty message")
    
    def _process(self, message: str, context: Dict) -> Any:
        """Core business logic"""
        pass
    
    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Return structured error"""
        return {
            "success": False,
            "error": {
                "code": type(error).__name__,
                "message": str(error)
            }
        }
✅ DO's
✅ Agent Design
One agent = One responsibility

Expose .get_help() method

Return structured responses ({success, data/error})

Validate ALL inputs

Log all operations

✅ Communication
Route through Orchestrator

Use standardized message format

Include agent name in responses

Provide helpful error messages

✅ Testing
Unit tests for each method

Integration tests with database

E2E tests with Orchestrator

Mock external APIs

Target 85%+ coverage

❌ DON'Ts
❌ Anti-Patterns
❌ Direct agent-to-agent calls

❌ Creating FallbackAgent or HelpAgent

❌ Agents doing multiple responsibilities

❌ Silent failures (no error messages)

❌ Hardcoded configuration

❌ Common Mistakes
❌ QueryAgent modifying data (should be read-only)

❌ Duplicate functionality between agents

❌ Not validating user input

❌ Exposing internal errors to users

❌ Not handling edge cases

🧪 Testing Checklist
For each agent:

 Unit tests: Individual methods work

 Integration tests: Database operations

 E2E tests: Full user workflows

 Error handling: All error paths covered

 Edge cases: Empty input, invalid data, conflicts

 Performance: Response time < 200ms

 Coverage: ≥ 85%

📊 Agent Comparison Matrix
Agent	Write	Read	External API	Milestone
AgendaAgent	✅	✅	Google Calendar	H09
QueryAgent	❌	✅	-	H10
NoteAgent	✅	✅	-	H10
ReminderAgent	✅	✅	-	H11
📖 Related Documentation
Agents Overview - All 4 agents architecture

SCHEMA.md - Complete system design

Orchestrator - Routing & coordination

FSM Engine - State machine patterns

Last Updated: 06 January 2026, 18:00 CET
Next Review: February 2026 (H10 completion)
Version: 2.0 - Aligned with 4-agent architecture
