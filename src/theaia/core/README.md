# CoreRouter

El módulo **CoreRouter** orquesta el enrutamiento de mensajes y la persistencia de contexto en la aplicación.  
Recibe un mensaje del usuario, detecta su intención, selecciona el agente adecuado y mantiene el estado entre interacciones.

## Flujo de procesamiento

1. **Detección temprana de intención**  
   - Se analiza el mensaje para identificar la intención (agenda, notas, evento, etc.).  
   - Si estamos en estado `initial` y la intención es desconocida (`fallback`),  
     se devuelve el mismo mensaje (eco) sin alterar el contexto.

2. **Recarga de contexto**  
   - Si el estado es `initial` y no hay contexto en memoria, se intenta  
     recargar el último estado y datos desde el repositorio JSON.

3. **Re-detección de intención**  
   - Tras la recarga de contexto, se vuelve a detectar la intención para  
     asegurar consistencia si el mensaje ya formaba parte de un flujo previo.

4. **Selección de agente**  
   - En `initial`, se elige el agente según la intención detectada (`agenda`, `notas`, etc.).  
   - En cualquier otro estado, se fuerza al **AgendaAgent** para continuar el flujo de citas.

5. **Inyección de metadatos en el contexto**  
   - `pending_intent`: intención detectada en esta interacción.  
   - `pending_datetime`: el texto del mensaje si no estamos en `initial`,  
     para ayudar en pruebas e2e del flujo de agendado.

6. **Delegación al agente**  
   - Se invoca `agent.process()`, pasando `user_id`, `message`, `current_state` y `current_data`.  
   - El agente retorna `response`, `new_state` y `new_data`.

7. **Persistencia de contexto**  
   - Se guarda en disco el nuevo estado y datos de contexto en el repositorio JSON.

## Ejemplo

from theaia.core.router import CoreRouter

router = CoreRouter()
uid = "user1"
state, context = "initial", {}

Usuario pide agendar
resp, state, context = router.handle(uid, "quiero agendar cita", state, context)

resp == "¿Para qué fecha y hora quieres agendar la cita?"
state == "awaiting_datetime"
text
undefined