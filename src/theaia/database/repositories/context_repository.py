import os, json
from threading import Lock

_lock = Lock()

def _get_path():
    return os.getenv("CONTEXT_DB_PATH", "context_store.json")

def _read_store():
    path = _get_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_store(store):
    path = _get_path()
    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(store, f)

def load_context(uid: str):
    store = _read_store()
    return store.get(uid)

def save_context(uid: str, state: str, data: dict):
    store = _read_store()
    store[uid] = {"state": state, "data": data}
    _write_store(store)
