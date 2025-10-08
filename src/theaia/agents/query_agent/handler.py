# src/theaia/agents/event_agent/handler.py

import json
from pathlib import Path
from theaia.agents.base_agent import BaseAgent
from theaia.models.context import UserContext

class EventAgent(BaseAgent):
    """
    Agente para gestionar eventos: crear, listar, modificar y cancelar.
    """
    INTENT = "create_event"

    def __init__(self):
        # Carga vocabulario
        vocab_path = Path(__file__).parent / "model" / "vocab.json"
        if vocab_path.exists():
            self.vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
        else:
            self.vocab = {}

    async def handle(self, text: str, ctx: UserContext, entities: dict):
        # Inicio de flujo: pedir título
        if ctx.state is None:
            ctx.state = "creating_event"
            return "¿Cuál es el título del evento?", ctx

        # Recibo el título, pido fecha
        if ctx.state == "creating_event":
            ctx.data["title"] = text
            ctx.state = "asking_date"
            return "¿Qué fecha y hora? (YYYY-MM-DD HH:MM)", ctx

        # Recibo la fecha, guardo el evento y cierro flujo
        if ctx.state == "asking_date":
            ctx.data["date"] = text
            # Aquí llamarías a tu servicio de eventos para persistir
            ctx.state = None
            return f"Evento «{ctx.data['title']}» para {ctx.data['date']} creado ✅", ctx

        # Caso por defecto
        return "No pude procesar tu solicitud de evento. Usa /help para más información.", ctx
