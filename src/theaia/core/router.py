# src/theaia/core/router.py

from theaia.ml.intent_detector import predict_intent
from theaia.core.context_manager import load_context, save_context
from theaia.agents.registry import agent_registry  # asume que tienes un registro de agentes

async def process_user_input(user_id: int, text: str):
    # 1. Carga contexto
    ctx = load_context(user_id)

    # 2. Detecta intención
    intent = predict_intent(text)

    # 3. Despacha al agente correspondiente
    agent = agent_registry.get(intent)
    response, new_ctx = await agent.handle(text, ctx)

    # 4. Persiste contexto actualizado
    save_context(new_ctx)

    return response, new_ctx
