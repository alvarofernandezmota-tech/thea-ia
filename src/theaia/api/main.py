# ======================================================
# THEA IA — API BÁSICA con FastAPI + Base de Datos JSON
# ======================================================

from fastapi import FastAPI
from src.theaia.database.json_storage import JsonDatabaseManager
from src.theaia.database.config import DATABASE_PATH

# Inicializar base JSON
db = JsonDatabaseManager(DATABASE_PATH)

# Crear instancia FastAPI
app = FastAPI(
    title="Thea IA API",
    description="API básica de Thea IA con almacenamiento JSON temporal",
    version="3.0.1"
)

# ------------------------------------------------------
# RUTA DE SALUD (para Render y Healthcheck)
# ------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "Thea IA API running successfully"}

# ------------------------------------------------------
# VER TODAS LAS NOTAS
# ------------------------------------------------------
@app.get("/notas")
def get_notas():
    notas = db.get_all("notas")
    return {"total": len(notas), "data": notas}

# ------------------------------------------------------
# INSERTAR UNA NUEVA NOTA
# ------------------------------------------------------
@app.post("/notas/{id}")
def create_nota(id: str, titulo: str, contenido: str):
    nueva = {"titulo": titulo, "contenido": contenido}
    db.insert("notas", id, nueva)
    return {"message": f"Nota {id} guardada correctamente", "data": nueva}

# ------------------------------------------------------
# OBTENER NOTA POR ID
# ------------------------------------------------------
@app.get("/notas/{id}")
def get_nota(id: str):
    nota = db.get("notas", id)
    if not nota:
        return {"error": f"No se encontró la nota {id}"}
    return nota

# ------------------------------------------------------
# ELIMINAR NOTA
# ------------------------------------------------------
@app.delete("/notas/{id}")
def delete_nota(id: str):
    if db.delete("notas", id):
        return {"message": f"Nota {id} eliminada"}
    return {"error": f"No existe la nota {id}"}
