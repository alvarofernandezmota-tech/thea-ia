from theaia.agents.scheduler_agent.handler import SchedulerAgent

def test_initial_to_awaiting_reminder_time():
    agent = SchedulerAgent()
    resp, state, data = agent.process('u1', 'quiero recordatorio', 'initial', {})
    assert 'cuándo' in resp.lower()
    assert state == 'awaiting_reminder_time'

def test_reminder_time_to_awaiting_message():
    agent = SchedulerAgent()
    resp, state, data = agent.process('u1', 'mañana a las 9', 'awaiting_reminder_time', {})
    assert 'mensaje' in resp.lower()
    assert state == 'awaiting_reminder_message'
    assert data['reminder_time'] == 'mañana a las 9'

def test_reminder_message_to_confirmation():
    agent = SchedulerAgent()
    current_data = {'reminder_time': 'mañana a las 9'}
    resp, state, data = agent.process('u1', 'llamar al médico', 'awaiting_reminder_message', current_data)
    assert 'confirmas' in resp.lower()
    assert state == 'awaiting_confirmation'
    assert data['reminder_message'] == 'llamar al médico'

def test_confirmation_completed():
    agent = SchedulerAgent()
    current_data = {'reminder_time': 'mañana a las 9', 'reminder_message': 'llamar al médico'}
    resp, state, data = agent.process('u1', 'sí', 'awaiting_confirmation', current_data)
    assert 'confirmado' in resp.lower()
    assert state == 'completed'
