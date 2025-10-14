# Tests del Core

Ubicación: `src/theaia/tests/core/`

Este directorio contiene los tests unitarios que validan el comportamiento de `CoreRouter` y componentes asociados.

## Archivos

- `test_core_basic.py`  
  - Verifica el manejo de estados iniciales y detección de intención.  
  - Casos: eco de fallback, enrutamiento a AgendaAgent, recarga de contexto.

- `test_router.py`  
  - Comprueba la selección de agentes según diferentes intenciones.  

- `test_context.py` y `test_context_manager.py`  
  - Validan la carga y persistencia de contexto de usuario.

- `test_callbacks.py`  
  - Asegura que los callbacks de eventos internos funcionen correctamente.

- `test_state_machine.py`  
  - Prueba utilidades de la máquina de estados.

## Ejecutar tests

pytest src/theaia/tests/core

text
undefined