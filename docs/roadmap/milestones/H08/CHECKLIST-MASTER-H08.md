# ✅ CHECKLIST MAESTRO H08 - Conversational Layer

**Hito:** H08
**Período:** 13 Diciembre 2025 (19:00 - 22:00 CET)
**Duración:** 3 horas
**Objetivo:** 🎯 Primera conversación REAL con agente integrado
**Status:** 🔵 EN CURSO
**Autor:** Álvaro Fernández Mota

---

## 📊 ESTADO GENERAL H08

INICIO: 13 Dic 19:00 CET
META: 42 tests, >85% coverage, conversación real
FIN: 13 Dic 22:00 CET

TIEMPO TOTAL: 3 horas

text

---

## 🚀 FASE 1: LLM Integration (30-45 min)

### ✅ 8.1.1 Create llm_client.py

**Archivo:** `src/theaia/core/conversation/llm_client.py`

☐ Step 1: Create directory
☐ mkdir -p src/theaia/core/conversation
☐ touch src/theaia/core/conversation/init.py

☐ Step 2: Implement LLMConfig class
☐ provider: str = "openai"
☐ model: str = "gpt-4-turbo"
☐ temperature: float = 0.7
☐ max_tokens: int = 2000
☐ timeout: int = 30
☐ max_retries: int = 3

☐ Step 3: Implement PromptTemplate class
☐ SYSTEM_PROMPT constant
☐ format_message() static method
☐ build_context() static method

☐ Step 4: Implement LLMClient class
☐ init with AsyncOpenAI
☐ generate_response() async method
☐ Retry logic with exponential backoff
☐ Error handling (OpenAIError)
☐ conversation_history management
☐ clear_history() method
☐ get_history() method
☐ close() async method

☐ Step 5: Implement MockLLMClient class
☐ For testing without API key
☐ Simple mock responses
☐ Same interface as LLMClient

☐ Step 6: Add docstrings
☐ Module docstring
☐ Class docstrings
☐ Method docstrings

STATUS: ☐ TODO → ☑️ DONE
TIME: 20 min

text

### ✅ 8.1.2 Create test_llm_client.py

**Archivo:** `src/theaia/tests/unit/conversation/test_llm_client.py`

☐ Step 1: Create test directory
☐ mkdir -p src/theaia/tests/unit/conversation
☐ touch src/theaia/tests/unit/conversation/init.py

☐ Step 2: Test LLMConfig
☐ test_llm_config_defaults
☐ test_llm_config_custom_values

☐ Step 3: Test PromptTemplate
☐ test_format_message
☐ test_build_context_empty_history
☐ test_build_context_with_history

☐ Step 4: Test MockLLMClient
☐ test_mock_generate_response
☐ test_mock_conversation_history

☐ Step 5: Test LLMClient (mock OpenAI)
☐ test_llm_client_initialization
☐ test_generate_response_mock

TESTS: 8 total
COVERAGE: >80%

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.1.3 First Commit

☐ git add src/theaia/core/conversation/
☐ git add src/theaia/tests/unit/conversation/
☐ git commit -m "feat(H08.1): add LLM client with OpenAI integration

LLMConfig with model/temperature/timeout settings

PromptTemplate for prompt management

LLMClient with retry logic and error handling

MockLLMClient for testing

8 unit tests, >80% coverage"
☐ git push origin main
☐ Verify: git log --oneline -1

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 🚀 FASE 2: Conversational Agent (45 min)

### ✅ 8.2.1 Create conversational_agent.py

**Archivo:** `src/theaia/core/conversation/conversational_agent.py`

☐ Step 1: Create main agent class
☐ ConversationalAgent(BaseAgent)
☐ Inherit from H07 BaseAgent if possible

☐ Step 2: Implement init
☐ self.llm_client: LLMClient
☐ self.coordination_engine: CoordinationEngine (H07.5)
☐ self.shared_context: SharedContext (H07.4)
☐ self.memory: ConversationMemory (H08.3)
☐ self.agent_id: str = "conversational_agent"
☐ self.personality: dict

☐ Step 3: Implement chat() async method
☐ Accept user_message: str
☐ Get user context from shared_context (H07.4)
☐ Build prompt with context
☐ Call llm_client.generate_response()
☐ Store in memory (H08.3)
☐ Return response: str

☐ Step 4: Implement _build_context() method
☐ Get user info from database (H02)
☐ Get conversation history
☐ Build context string

☐ Step 5: Implement coordination() method
☐ Use CoordinationEngine (H07.5) if complex
☐ For simple: direct LLM call

☐ Step 6: Add docstrings
☐ Module docstring
☐ Class docstring
☐ Method docstrings

STATUS: ☐ TODO → ☑️ DONE
TIME: 25 min

text

### ✅ 8.2.2 Create agent_config.py

**Archivo:** `src/theaia/core/conversation/agent_config.py`

☐ Step 1: Create AgentConfig class
☐ name: str = "THEA"
☐ personality: str = "helpful, friendly, professional"
☐ tone: str = "conversational"
☐ max_history: int = 20

☐ Step 2: Create system prompts
☐ SYSTEM_PROMPT_DEFAULT
☐ SYSTEM_PROMPT_PROFESSIONAL
☐ SYSTEM_PROMPT_FRIENDLY

☐ Step 3: Add method to get prompt
☐ get_system_prompt(tone: str) -> str

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.2.3 Create test_conversational_agent.py

**Archivo:** `src/theaia/tests/unit/conversation/test_conversational_agent.py`

☐ Step 1: Test agent initialization
☐ test_agent_creation
☐ test_agent_with_config

☐ Step 2: Test chat method
☐ test_simple_chat
☐ test_chat_with_context
☐ test_chat_history_tracking

☐ Step 3: Test context building
☐ test_build_context_empty
☐ test_build_context_with_history

☐ Step 4: Test H07 integration
☐ test_coordination_engine_integration
☐ test_shared_context_integration

TESTS: 10 total
COVERAGE: >80%

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.2.4 Second Commit

☐ git add src/theaia/core/conversation/conversational_agent.py
☐ git add src/theaia/core/conversation/agent_config.py
☐ git add src/theaia/tests/unit/conversation/test_conversational_agent.py
☐ git commit -m "feat(H08.2): add conversational agent with H07 integration

ConversationalAgent class (async chat)

Integration with H07 CoordinationEngine

Integration with H07 SharedContext

AgentConfig with system prompts

10 unit tests, >80% coverage"
☐ git push origin main
☐ Verify: git log --oneline -2

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 🚀 FASE 3: Memory System (30 min)

### ✅ 8.3.1 Create memory.py

**Archivo:** `src/theaia/core/conversation/memory.py`

☐ Step 1: Create ConversationMemory class
☐ self.messages: List[Dict]
☐ self.session_id: str
☐ self.user_id: str
☐ self.created_at: datetime
☐ self.max_size: int = 100

☐ Step 2: Implement add_message() method
☐ Accept role: str, content: str
☐ Add timestamp
☐ Maintain max_size

☐ Step 3: Implement get_history() method
☐ Return last N messages
☐ Default N = 10

☐ Step 4: Implement search() method
☐ Search in history by keyword
☐ Return matching messages

☐ Step 5: Implement clear() method
☐ Clear all messages

☐ Step 6: Add database integration
☐ save_to_db() - persist to H02
☐ load_from_db() - load conversation

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.3.2 Create context_builder.py

**Archivo:** `src/theaia/core/conversation/context_builder.py`

☐ Step 1: Create ContextBuilder class
☐ build_prompt_context() method
☐ build_agent_context() method

☐ Step 2: Implement context formatting
☐ Format history as string
☐ Add user info
☐ Add session info

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.3.3 Create test_memory.py

**Archivo:** `src/theaia/tests/unit/conversation/test_memory.py`

☐ test_memory_creation
☐ test_add_message
☐ test_get_history
☐ test_search_messages
☐ test_clear_memory
☐ test_save_to_db
☐ test_load_from_db
☐ test_max_size_limit

TESTS: 8 total
COVERAGE: >80%

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.3.4 Third Commit

☐ git add src/theaia/core/conversation/memory.py
☐ git add src/theaia/core/conversation/context_builder.py
☐ git add src/theaia/tests/unit/conversation/test_memory.py
☐ git commit -m "feat(H08.3): add conversation memory system

ConversationMemory with history management

Database persistence (H02)

Search and retrieval

ContextBuilder for context formatting

8 unit tests, >80% coverage"
☐ git push origin main

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 🚀 FASE 4: Tool Calling (30 min)

### ✅ 8.4.1 Create tools.py

**Archivo:** `src/theaia/core/conversation/tools.py`

☐ Step 1: Create ToolRegistry class
☐ Register tools
☐ Get tool definitions
☐ List available tools

☐ Step 2: Create Tool base class
☐ name: str
☐ description: str
☐ parameters: Dict
☐ execute() method

☐ Step 3: Create sample tools
☐ SearchTool (H07 agents)
☐ DatabaseTool (H02)
☐ CalculatorTool

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.4.2 Create tool_executor.py

**Archivo:** `src/theaia/core/conversation/tool_executor.py`

☐ Step 1: Create ToolExecutor class
☐ execute_tool() method
☐ Validate parameters
☐ Call tool
☐ Handle errors

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.4.3 Create test_tools.py

**Archivo:** `src/theaia/tests/unit/conversation/test_tools.py`

☐ test_tool_registry
☐ test_tool_registration
☐ test_tool_execution
☐ test_invalid_parameters
☐ test_tool_error_handling
☐ test_executor

TESTS: 6 total
COVERAGE: >80%

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.4.4 Fourth Commit

☐ git add src/theaia/core/conversation/tools.py
☐ git add src/theaia/core/conversation/tool_executor.py
☐ git add src/theaia/tests/unit/conversation/test_tools.py
☐ git commit -m "feat(H08.4): add tool calling system

ToolRegistry for managing tools

Tool base class and sample tools

ToolExecutor for safe execution

Integration with H07 agents

6 unit tests, >80% coverage"
☐ git push origin main

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 🚀 FASE 5: CLI Interface (30 min)

### ✅ 8.5.1 Create cli.py

**Archivo:** `src/theaia/core/conversation/cli.py`

☐ Step 1: Create CLI class
☐ init with agent
☐ welcome message
☐ help text

☐ Step 2: Implement main loop
☐ Read user input
☐ Call agent.chat()
☐ Display response
☐ Handle commands (/exit, /clear, /history)

☐ Step 3: Implement run() method
☐ Main entry point
☐ Async handling
☐ Error handling

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.5.2 Create utils.py

**Archivo:** `src/theaia/core/conversation/utils.py`

☐ Step 1: Create utility functions
☐ format_response() - pretty print
☐ format_error() - error display
☐ format_help() - help text
☐ wrap_text() - text wrapping

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.5.3 Create test_cli.py

**Archivo:** `src/theaia/tests/unit/conversation/test_cli.py`

☐ test_cli_creation
☐ test_user_input_handling
☐ test_response_display
☐ test_command_processing
☐ test_exit_command

TESTS: 5 total
COVERAGE: >80%

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.5.4 Fifth Commit

☐ git add src/theaia/core/conversation/cli.py
☐ git add src/theaia/core/conversation/utils.py
☐ git add src/theaia/tests/unit/conversation/test_cli.py
☐ git commit -m "feat(H08.5): add CLI interface

Interactive chat loop

Command processing (/exit, /clear, /history)

Pretty printing and formatting

Error handling

5 unit tests, >80% coverage"
☐ git push origin main

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 🚀 FASE 6: Integration Tests & First Conversation (30 min)

### ✅ 8.6.1 Create test_conversation_e2e.py

**Archivo:** `src/theaia/tests/integration/test_conversation_e2e.py`

☐ Step 1: Setup integration tests
☐ Create test database
☐ Initialize agent
☐ Setup LLM mock

☐ Step 2: Test simple conversation
☐ test_single_turn_conversation
☐ Verify response generated
☐ Verify in history

☐ Step 3: Test multi-turn conversation
☐ test_multi_turn_conversation
☐ Multiple back-and-forth
☐ Context maintained

☐ Step 4: Test agent coordination
☐ test_with_h07_coordination
☐ Verify CoordinationEngine used
☐ Verify locks working

☐ Step 5: Test database access
☐ test_h02_database_access
☐ Store conversation
☐ Retrieve conversation

TESTS: 5 integration tests
COVERAGE: >85%

STATUS: ☐ TODO → ☑️ DONE
TIME: 15 min

text

### ✅ 8.6.2 Run All Tests

☐ pytest src/theaia/tests/unit/conversation/ -v
☐ Expect: 29 tests passing
☐ Coverage: >80%

☐ pytest src/theaia/tests/integration/test_conversation_e2e.py -v
☐ Expect: 5 tests passing
☐ Coverage: >85%

☐ Total: 34+ tests passing

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

### ✅ 8.6.3 First Real Conversation

☐ Step 1: Setup environment
☐ export OPENAI_API_KEY=your_key (or use mock)
☐ Verify database running

☐ Step 2: Start CLI
☐ python -m theaia.core.conversation.cli

☐ Step 3: Have conversation
User: "Hello, what is your name?"
Agent: "I'm THEA, an advanced AI assistant..."

User: "Remember my name is Álvaro"
Agent: "Nice to meet you, Álvaro!"

User: "What did I just tell you?"
Agent: "You told me your name is Álvaro"

User: "/exit"
Agent: "Goodbye!"

STATUS: ☐ TODO → ☑️ DONE
TIME: 10 min

text

### ✅ 8.6.4 Sixth Commit - Final

☐ git add src/theaia/tests/integration/test_conversation_e2e.py
☐ git commit -m "feat(H08): complete conversational layer with integration tests

Summary
✅ 42 tests (37 unit + 5 integration)
✅ >85% coverage
✅ LLM integration (OpenAI + mock)
✅ Conversational agent with H07 coordination
✅ Memory system with database persistence
✅ Tool calling framework
✅ CLI interface for interactive chat
✅ First REAL conversation working

Modules
8.1 LLM Client (llm_client.py)

8.2 Conversational Agent (conversational_agent.py)

8.3 Memory System (memory.py)

8.4 Tool Calling (tools.py)

8.5 CLI Interface (cli.py)

Integration
✅ Uses H06 FSM
✅ Uses H07 CoordinationEngine
✅ Uses H07 SharedContext
✅ Uses H02 Database

Status: H08 PRODUCTION-READY - First real conversation validated"
☐ git push origin main

STATUS: ☐ TODO → ☑️ DONE
TIME: 5 min

text

---

## 📊 CHECKLIST FINAL H08

### ✅ Code Implementation (5 modules)
☐ llm_client.py (LLMConfig, PromptTemplate, LLMClient, MockLLMClient)
☐ conversational_agent.py (ConversationalAgent with H07 integration)
☐ agent_config.py (AgentConfig, system prompts)
☐ memory.py (ConversationMemory, database persistence)
☐ context_builder.py (ContextBuilder)
☐ tools.py (ToolRegistry, Tool base, sample tools)
☐ tool_executor.py (ToolExecutor)
☐ cli.py (CLI class, main loop)
☐ utils.py (Formatting utilities)

text

### ✅ Tests (42 total)
☐ 8 tests: test_llm_client.py
☐ 10 tests: test_conversational_agent.py
☐ 8 tests: test_memory.py
☐ 6 tests: test_tools.py
☐ 5 tests: test_cli.py
☐ 5 integration: test_conversation_e2e.py
→ TOTAL: 42 tests, 100% passing
→ Coverage: >85%

text

### ✅ Integration Points
☐ H07.5 CoordinationEngine (coordination)
☐ H07.4 SharedContext (memory)
☐ H07.1 AgentRegistry (agent discovery)
☐ H02 Database (persistence)
☐ H06 FSM (internal state)

text

### ✅ Documentation
☐ Docstrings in all modules
☐ README for H08
☐ Usage examples in tests
☐ Architecture diagram (if needed)

text

### ✅ Git Commits (6 commits)
☐ Commit 1: feat(H08.1) - LLM Client
☐ Commit 2: feat(H08.2) - Conversational Agent
☐ Commit 3: feat(H08.3) - Memory System
☐ Commit 4: feat(H08.4) - Tool Calling
☐ Commit 5: feat(H08.5) - CLI Interface
☐ Commit 6: feat(H08) - Integration & First Conversation

text

---

## 🎯 SUCCESS CRITERIA

### ✅ All Criteria Met?
☐ 42 tests written
☐ 42/42 tests passing (100%)
☐ >85% coverage achieved
☐ Real conversation tested manually
☐ H06+H07 integration proven
☐ H02 database access working
☐ All commits pushed
☐ No errors in tests
☐ No warnings in code
☐ Documentation complete

text

---

## ⏱️ TIME TRACKING

FASE 1: LLM Integration 30-45 min ☐
FASE 2: Conversational Agent 45 min ☐
FASE 3: Memory System 30 min ☐
FASE 4: Tool Calling 30 min ☐
FASE 5: CLI Interface 30 min ☐
FASE 6: Integration Tests 30 min ☐
─────────────────────────────────────────
TOTAL: 3 hours ☐

START TIME: 19:00 CET
TARGET END: 22:00 CET

text

---

## 🎉 FINAL STATUS

**When all checkboxes are ☑️:**

✅ H08 CONVERSATIONAL LAYER COMPLETE
✅ 42 tests passing (100%)
✅ >85% coverage achieved
✅ Real conversation working
✅ MVP Multi-Agent System PRODUCTION-READY
✅ Ready for H09 (Web UI)

🎊 THEA AGENT CAN HAVE REAL CONVERSATIONS! 🎊

text

---

## 📌 Notes

- **Environment:** Set OPENAI_API_KEY or use MockLLMClient
- **Database:** Must be running (PostgreSQL)
- **Python:** 3.9+
- **Time:** 3 hours max
- **Momentum:** Keep it up! 🚀

---

**Versión:** 1.0
**Fecha:** 13 Diciembre 2025
**Status:** 🔵 EN CURSO - ¡A COMENZAR!
🚀 ¿COMENZAMOS H08?
bash
# 1. Crear archivo
code CHECKLIST-MASTER-H08.md
# (Pega el contenido completo arriba)

# 2. Git
git add CHECKLIST-MASTER-H08.md
git commit -m "docs: add H08 master checklist for conversational layer implementation"
git push origin main

# 3. COMENZAR FASE 1
# mkdir -p src/theaia/core/conversation
# code src/theaia/core/conversation/llm_client.py
¿VAMOS A CREAR LA CONVERSACIÓN REAL AHORA? 🎉🚀