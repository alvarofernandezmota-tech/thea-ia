"""
Repositorio de Contextos - Thea IA 3.0
-------------------------------------

Módulo responsable de almacenar y recuperar el contexto conversacional de cada usuario.
Diseñado para integrarse con el ecosistema FSM multiagente (CoreRouter).

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


# -------------------- UTILIDADES INTERNAS --------------------

def _get_path() -> str:
    """Devuelve la ruta del archivo de almacenamiento del contexto global."""
    return os.getenv("CONTEXT_DB_PATH", "context_store.json")


def _read_store() -> Dict[str, Any]:
    """Lee la estructura JSON del contexto global."""
    path = _get_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"[ADVERTENCIA] El archivo '{path}' estaba vacío o corrupto. Reiniciado.")
        return {}


def _write_store(store: Dict[str, Any]):
    """Escribe el diccionario completo de contextos al disco."""
    path = _get_path()
    with _lock:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Fallo al escribir el archivo de contexto: {e}")


# -------------------- FUNCIONES PÚBLICAS --------------------

def load_context(user_id: str) -> Dict[str, Any] | None:
    """Recupera el contexto de un usuario específico."""
    store = _read_store()
    return store.get(user_id)


def save_context(user_id: str, state: str, context: Dict[str, Any]):
    """
    Guarda o actualiza el contexto completo de un usuario.

    Este formato de tres parámetros (user_id, state, context)
    mantiene compatibilidad con los tests y el flujo FSM global.
    """
    if not isinstance(context, dict):
        raise ValueError("El parámetro 'context' debe ser un diccionario válido.")

    store = _read_store()
    store[user_id] = {"state": state, "data": context}
    _write_store(store)


def clear_context(user_id: str | None = None):
    """Borra uno o todos los contextos almacenados."""
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
        print("[Thea IA] Todos los contextos fueron eliminados exitosamente.")
