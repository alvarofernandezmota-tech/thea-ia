# src/theaia/tests/core/test_callbacks.py

from src.theaia.core.callbacks import (
    handle_agenda, handle_scheduler, handle_event, handle_note,
    handle_query, handle_help, handle_fallback, handle_completed, handle_error
)

def test_handle_agenda():
    assert handle_agenda({}) == "Agenda gestionada correctamente."

def test_handle_scheduler():
    assert handle_scheduler({}) == "Tarea programada correctamente."

def test_handle_event():
    assert handle_event({}) == "Evento registrado correctamente."

def test_handle_note():
    assert handle_note({}) == "Nota guardada correctamente."

def test_handle_query():
    assert handle_query({}) == "Consulta respondida correctamente."

def test_handle_help():
    assert handle_help({}) == "Ayuda de Thea IA mostrada."

def test_handle_fallback():
    assert handle_fallback({}) == "No se entendió la petición. Fallback aplicado."

def test_handle_completed():
    assert handle_completed({}) == "Conversación completada correctamente."

def test_handle_error():
    assert handle_error({}) == "Error en flujo conversacional."
