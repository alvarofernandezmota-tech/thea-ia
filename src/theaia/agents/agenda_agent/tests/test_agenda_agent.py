from theaia.agents.agenda_agent.handler import AgendaAgent

def test_initial_to_awaiting_datetime():
    agent = AgendaAgent()
    resp, state, data = agent.process('u1', 'quiero agendar cita', 'initial', {})
    assert 'fecha y hora' in resp.lower()
    assert state == 'awaiting_datetime'

def test_awaiting_datetime_to_confirmation():
    agent = AgendaAgent()
    resp, state, data = agent.process('u1', '2025-10-10 09:00', 'awaiting_datetime', {})
    assert 'confirmas' in resp.lower()
    assert state == 'awaiting_confirmation'
    assert data['appointment_datetime'] == '2025-10-10 09:00'

def test_confirmation_completed():
    agent = AgendaAgent()
    resp, state, data = agent.process('u1', 'sí', 'awaiting_confirmation', {'appointment_datetime':'2025-10-10 09:00'})
    assert 'confirmada' in resp.lower()
    assert state == 'completed'
