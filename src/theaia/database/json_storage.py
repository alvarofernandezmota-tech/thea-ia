# ======================================================
# THEA IA — Módulo de almacenamiento JSON
# Versión simplificada y adaptada a Thea IA 3.0
# ======================================================

import os
import json
from datetime import datetime
from threading import Lock

class JsonDatabaseManager:
    def __init__(self, path: str = "./src/theaia/database/theaia_db.json"):
        self.path = path
        self.lock = Lock()
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Si el archivo no existe, se crea vacío
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

    # ---------------------------------------------
    # Cargar el contenido actual de la base
    # ---------------------------------------------
    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------------------------------------
    # Guardar cambios en disco
    # ---------------------------------------------
    def _save(self, data: dict):
        with self.lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    # ---------------------------------------------
    # Insertar o actualizar elemento
    # ---------------------------------------------
    def insert(self, collection: str, key: str, value: dict):
        data = self._load()
        if collection not in data:
            data[collection] = {}
        value["updated_at"] = datetime.utcnow().isoformat()
        data[collection][key] = value
        self._save(data)
        return True

    # ---------------------------------------------
    # Obtener una colección completa
    # ---------------------------------------------
    def get_all(self, collection: str):
        data = self._load()
        return data.get(collection, {})

    # ---------------------------------------------
    # Obtener un elemento concreto
    # ---------------------------------------------
    def get(self, collection: str, key: str):
        data = self._load()
        return data.get(collection, {}).get(key)

    # ---------------------------------------------
    # Eliminar elemento
    # ---------------------------------------------
    def delete(self, collection: str, key: str):
        data = self._load()
        if collection in data and key in data[collection]:
            del data[collection][key]
            self._save(data)
            return True
        return False
