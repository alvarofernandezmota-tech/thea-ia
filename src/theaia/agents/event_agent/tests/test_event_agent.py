from theaia.agents.event_agent.handler import EventAgent

def test_initial_to_awaiting_event_type():
    agent = EventAgent()
    resp, state, data = agent.process('u1', 'quiero evento', 'initial', {})
    assert 'tipo de evento' in resp.lower()
    assert state == 'awaiting_event_type'

def test_event_type_to_awaiting_datetime():
    agent = EventAgent()
    resp, state, data = agent.process('u1', 'reunión', 'awaiting_event_type', {})
    assert 'fecha y hora' in resp.lower()
    assert state == 'awaiting_event_datetime'
    assert data['event_type'] == 'reunión'

def test_event_datetime_to_confirmation():
    agent = EventAgent()
    current_data = {'event_type': 'reunión'}
    resp, state, data = agent.process('u1', '2025-10-10 09:00', 'awaiting_event_datetime', current_data)
    assert 'confirmas' in resp.lower()
    assert state == 'awaiting_event_confirmation'
    assert data['event_datetime'] == '2025-10-10 09:00'

def test_confirmation_completed():
    agent = EventAgent()
    current_data = {'event_type': 'reunión', 'event_datetime': '2025-10-10 09:00'}
    resp, state, data = agent.process('u1', 'sí', 'awaiting_event_confirmation', current_data)
    assert 'confirmado' in resp.lower()
    assert state == 'completed'

def test_event_cancellation():
    agent = EventAgent()
    current_data = {'event_type': 'reunión', 'event_datetime': '2025-10-10 09:00'}
    resp, state, data = agent.process('u1', 'no', 'awaiting_event_confirmation', current_data)
    assert 'cancelado' in resp.lower()
    assert state == 'initial'
    assert data == {}
