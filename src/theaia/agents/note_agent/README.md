# NoteAgent

Ubicación: `src/theaia/agents/note_agent/`

El **NoteAgent** permite al usuario crear y gestionar notas rápidas.

## Flujo de interacción completado

1. **initial**  
   - Solicita el contenido de la nota.  
   - Response: “¿Qué quieres anotar?”  
   - Nuevo estado: `awaiting_note_content`

2. **awaiting_note_content**  
   - Recibe el texto de la nota y la guarda.  
   - Response: “Nota guardada: {contenido}”  
   - Nuevo estado: `completed`

3. **completed**  
   - Fin del flujo.

## Ejemplo de uso

from theaia.agents.note_agent.handler import NoteAgent

agent = NoteAgent()
state, data = "initial", {}

Paso 1
resp, state, data = agent.process("u1", "apuntar nota", state, data)

-> "¿Qué quieres anotar?" (awaiting_note_content)
text

## Ejecutar tests

pytest src/theaia/agents/note_agent/tests

text
undefined