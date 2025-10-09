from theaia.agents.note_agent.handler import NoteAgent


def test_initial_to_awaiting_note_text():
    agent = NoteAgent()
    resp, state, data = agent.process('u1', 'quiero guardar una nota', 'initial', {})
    assert 'guardar' in resp.lower()
    assert state == 'awaiting_note_text'

def test_awaiting_note_text_to_completed():
    agent = NoteAgent()
    resp, state, data = agent.process('u1', 'Compra pan y leche', 'awaiting_note_text', {})
    assert 'guardada' in resp.lower()
    assert state == 'completed'
    assert data['note_text'] == 'Compra pan y leche'
