"""
Repositorio de Contextos - Thea IA 3.0
-------------------------------------

Módulo responsable de almacenar y recuperar el contexto conversacional de cada usuario.
Está diseñado para integrarse con el ecosistema FSM multiagente (CoreRouter).

Características:
- Thread-safe (usa Lock para evitar escrituras simultáneas).
- Persistencia en un único archivo JSON configurable por variable de entorno.
- Estructura escalable: { user_id: { "state": str, "data": dict } }.
- Preparado para migración a base de datos real sin cambiar la API pública.
"""

import os
import json
from threading import Lock
from typing import Dict, Any

# Bloqueo global para garantizar integridad de escritura concurrente
_lock = Lock()

# -----------------------------------------------------------------------------
#                     UTILIDADES INTERNAS
# -----------------------------------------------------------------------------
def _get_path() -> str:
    """
    Devuelve la ruta del archivo de almacenamiento del contexto global.
    Puede definirse por variable de entorno CONTEXT_DB_PATH.
    """
    return os.getenv("CONTEXT_DB_PATH", "context_store.json")


def _read_store() -> Dict[str, Any]:
    """
    Lee la estructura JSON de contexto global.
    Si el archivo no existe o está corrupto, devuelve un diccionario vacío.
    """
    path = _get_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"[Advertencia] El archivo de contexto '{path}' estaba vacío o corrupto. Reiniciado.")
        return {}


def _write_store(store: Dict[str, Any]):
    """
    Escribe el diccionario completo de contextos al disco.
    Usa un Lock para evitar colisiones si múltiples hilos escriben a la vez.
    """
    path = _get_path()
    with _lock:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Error de escritura en contexto] {e}")

# -----------------------------------------------------------------------------
#                     FUNCIONES PÚBLICAS DE ACCESO
# -----------------------------------------------------------------------------
def load_context(user_id: str) -> Dict[str, Any] | None:
    """
    Recupera el contexto de un usuario específico.
    Si no existe, devuelve None.
    """
    store = _read_store()
    return store.get(user_id)


def save_context(user_id: str, data: dict):
    """
    Guarda o actualiza el contexto completo de un usuario.
    
    Parámetros:
        user_id: str -> identificador único del usuario.
        data: dict   -> diccionario completo del contexto (debe incluir 'fsm_state' internamente).
    
    Ejemplo almacenado:
    {
        "u123": {
            "state": "awaiting_text",
            "data": {
                "delegated_intent": "nota",
                "fsm_state": "awaiting_text",
                "notes": [...]
            }
        }
    }
    """
    if not isinstance(data, dict):
        raise ValueError("El parámetro 'data' debe ser un diccionario válido.")
    
    store = _read_store()
    
    # Extraer el estado desde 'data' si existe, o usar un estado por defecto
    state = data.get("fsm_state", "initial")
    
    store[user_id] = {"state": state, "data": data}
    _write_store(store)

# -----------------------------------------------------------------------------
#                     UTILIDAD DE LIMPIEZA (OPCIONAL)
# -----------------------------------------------------------------------------
def clear_context(user_id: str | None = None):
    """
    Si se proporciona un user_id, borra solo ese contexto.
    Si no, limpia todos los contextos almacenados.
    """
    if user_id:
        store = _read_store()
        if user_id in store:
            store.pop(user_id)
            _write_store(store)
            print(f"[Thea IA] Contexto del usuario '{user_id}' eliminado correctamente.")
        else:
            print(f"[Thea IA] No existe contexto para el usuario '{user_id}'.")
    else:
        _write_store({})
        print("[Thea IA] Todos los contextos fueron eliminados con éxito.")
