import sys
import os
import pytest

# Corrige path para importar theaia aunque pytest no ajuste PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from theaia.core.router import CoreRouter

@pytest.mark.e2e
def test_notas_flow():
    router = CoreRouter()
    uid = "test_notas_1"
    state = "initial"
    context = {}

    # Paso 1: iniciar creación de nota
    resp, state, context = router.handle(uid, "quiero guardar una nota", state, context)
    assert any(
        palabra in resp.lower()
        for palabra in [
            "contenido",
            "¿qué quieres guardar",
            "escribe tu nota",
            "dime el texto",
            "qué nota quieres guardar"
        ]
    ), f'Respuesta inesperada en paso 1: "{resp}"'
    assert state == "awaiting_note_text"

    # Paso 2: escribir nota (usa una frase inequívoca)
    nota_texto = "Nota: entregar el informe de Thea IA antes del viernes"
    resp, state, context = router.handle(uid, nota_texto, state, context)
    assert any(
        palabra in resp.lower()
        for palabra in [
            "confirmas",
            "seguro",
            "quieres guardar",
            "¿guardamos esta nota"
        ]
    ), f'Respuesta inesperada en paso 2: "{resp}"'
    assert state == "awaiting_confirmation"

    # Paso 3: cancelar opción negativa
    resp, state, context = router.handle(uid, "no", state, context)
    assert any(
        palabra in resp.lower()
        for palabra in [
            "operación cancelada",
            "no se guardó",
            "nota descartada"
        ]
    ), f'Respuesta inesperada en paso 3 (no): "{resp}"'
    assert state == "initial"

    # Paso 4: repetir el flujo y confirmar
    resp, state, context = router.handle(uid, "quiero guardar una nota", state, context)
    assert state == "awaiting_note_text"

    resp, state, context = router.handle(uid, nota_texto, state, context)
    assert state == "awaiting_confirmation"

    resp, state, context = router.handle(uid, "sí", state, context)
    assert any(
        kw in resp.lower()
        for kw in [
            "nota guardada",
            "tu nota ha sido registrada",
            "guardada",
            "he anotado"
        ]
    ), f'Respuesta inesperada en paso 4 (sí): "{resp}"'
    assert state == "completed"

    # Verifica que la nota ha quedado en el contexto
    assert "last_note" in context, "No se encontró la clave 'last_note' en el contexto"
    content = context["last_note"].get("content", "")
    assert nota_texto.lower() in content.lower(), f'El contenido guardado es: "{content}"'

    # (Opcional) - comprobar timestamp si existe
    if "created_at" in context["last_note"]:
        assert isinstance(context["last_note"]["created_at"], str)
