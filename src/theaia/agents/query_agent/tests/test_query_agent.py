from theaia.agents.query_agent.handler import QueryAgent

def test_query_cita():
    agent = QueryAgent()
    data = {'appointment_datetime': '2025-10-10 09:00'}
    resp, state, result_data = agent.process('u1', '¿Qué cita tengo?', 'initial', data)
    assert '2025-10-10' in resp
    assert state == 'completed'

def test_query_nota():
    agent = QueryAgent()
    data = {'note_text': 'Comprar pan'}
    resp, state, result_data = agent.process('u1', '¿Qué nota tengo?', 'initial', data)
    assert 'Comprar pan' in resp
    assert state == 'completed'

def test_query_evento():
    agent = QueryAgent()
    data = {'event_type': 'reunión'}
    resp, state, result_data = agent.process('u1', '¿Qué evento tengo?', 'initial', data)
    assert 'reunión' in resp
    assert state == 'completed'
