Router — TheaRouter Entry Point para THEA IA
Versión: v1.0
Ubicación: src/theaia/core/router.py
Última actualización: 2025-11-10 16:00 CET (S38)
Estado: ✅ Production Ready

📖 Overview
TheaRouter es el único entry point para toda comunicación conversacional en THEA IA 2.0.

Funciona como director de orquesta que:

Valida usuario y crea/recupera sesión

Detecta intención (ML)

Gestiona FSM por usuario

Retorna respuesta + contexto

🔑 Clase Principal
python
class TheaRouter:
    def __init__(self, intent_detector, context_manager)
    
    def handle_request(self, user_id: str, message: str) 
        → Tuple[str, Dict[str, Any]]
📋 Métodos
handle_request(user_id, message)
Flujo:

text
1. Validar user_id
   ├─ Crear session si no existe
   └─ Recuperar contexto anterior

2. Detectar intents
   ├─ IntentDetector.predict(message)
   └─ Scores + top-3 intents

3. Get/Create FSM
   ├─ Si user_id es nuevo → crear ConversationManager
   └─ Si existe → recuperar

4. Process through FSM
   ├─ fsm.process_input(message, intents)
   └─ Retorna: response, state, updated_context

5. Update stored context
   ├─ context_manager.update(user_id, context)
   └─ Persistir sesión

6. Return to client
   └─ (response, updated_context)
💡 Ejemplo Uso
python
from src.theaia.core.router import TheaRouter

router = TheaRouter()

response, context = router.handle_request(
    user_id="alvaro_123",
    message="Quiero agendar una reunión"
)

print(response)
# Output: "¿Para qué fecha quieres agendar?"

print(context['current_state'])
# Output: "agent_delegated"
🔌 Integración
REST API
python
@app.post("/chat")
async def chat(user_id: str, message: str):
    response, context = router.handle_request(user_id, message)
    return {"response": response, "state": context.get('current_state')}
WebSocket
python
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        response, _ = router.handle_request(user_id, message)
        await websocket.send_json({"response": response})
📊 Propiedades
Propiedad	Tipo	Descripción
managers	Dict	FSMs por user_id
context_manager	ContextManager	Gestor contexto
intent_detector	IntentDetector	Detector ML
🐛 Known Issues
 Sin rate limiting (v1.0)

 Sin validación input sanitization (v1.0)

 Managers en memoria → Redis v1.1

Última actualización: 2025-11-10 16:00 CET