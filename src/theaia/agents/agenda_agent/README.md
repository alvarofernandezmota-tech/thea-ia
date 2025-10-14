# AgendaAgent

Ubicación: `src/theaia/agents/agenda_agent/`

El **AgendaAgent** gestiona el flujo completo de agendado de citas con un usuario.

## Flujo de interacción completado

1. **initial**  
   - Solicita la fecha y hora de la cita.  
   - Response: [translate:¿Para qué fecha y hora quieres agendar la cita?]  
   - Nuevo estado: `awaiting_datetime`

2. **awaiting_datetime**  
   - Recibe una cadena ISO `YYYY-MM-DD HH:MM`.  
   - Si el formato es inválido:  
     - Response: [translate:No entendí la fecha. Por favor usa formato YYYY-MM-DD HH:MM]  
     - Estado sigue siendo `awaiting_datetime`  
   - Si es válido:  
     - Guarda `appointment_datetime` en el contexto.  
     - Response: `Confirmas la cita para {appointment_datetime}?`  
     - Nuevo estado: `awaiting_confirmation`

3. **awaiting_confirmation**  
   - Espera confirmación (sí/si/confirmo).  
   - Si confirma:  
     - Guarda en `last_event` un diccionario con  
       - `uid`: identificador de usuario  
       - `type`: `"appointment"`  
       - `datetime`: fecha agendada  
     - Response: `Cita confirmada para {datetime}. ¡Listo!`  
     - Nuevo estado: `completed`  
   - Si no confirma:  
     - Response: [translate:Solicitud cancelada. ¿Necesitas otra cosa?]  
     - Nuevo estado: `initial`

4. **completed**  
   - Fin del flujo.

## Ejemplo de uso

from theaia.agents.agenda_agent.handler import AgendaAgent

agent = AgendaAgent()
state, data = "initial", {}

Paso 1
resp, state, data = agent.process("u1", "quiero agendar cita", state, data)

-> "¿Para qué fecha y hora quieres agendar la cita?" (awaiting_datetime)
text

## Ejecutar tests

pytest src/theaia/agents/agenda_agent/tests

text
undefined