# ======================================================
# CONFIGURACIÓN BÁSICA DE THEA IA
# Compatible con almacenamiento JSON local
# ======================================================

import os
import json
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# --- VARIABLES DE ENTORNO ---
DATABASE_MODE = os.getenv("DATABASE_MODE", "json")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./src/theaia/database/theaia_db.json")
THEA_ENV = os.getenv("THEA_ENV", "development")
APP_NAME = os.getenv("APP_NAME", "thea-ia")

# --- ASEGURAR BASE DE DATOS JSON ---
def init_database():
    """
    Si no existe la base JSON, la crea vacía.
    """
    path = DATABASE_PATH
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
            print(f"✅ Creado nuevo archivo de base de datos: {path}")
    else:
        print(f"📚 Base de datos existente: {path}")

# Ejecutar la creación automática
if __name__ == "__main__":
    init_database()
    print("💡 Thea IA configurada correctamente.")
