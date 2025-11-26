🧪 Schedule Agent Tests
Coverage: 85%+ | v1.0.0

📊 Test Suite
test_handler.py:

✅ test_schedule_agent_init()

✅ test_get_supported_intents()

✅ test_handle_day_input()

✅ test_handle_action_input()

test_schedule_fsm.py:

✅ test_fsm_init()

✅ test_day_transition()

✅ test_action_transition()

✅ test_state_persistence()

🏃 Ejecutar
bash
pytest src/theaia/agents/schedule_agent/tests/ -v
Schedule Tests v1.0