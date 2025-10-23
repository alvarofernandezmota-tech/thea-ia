# ============================================================
# THEA IA 3.0 — MAIN API BÁSICA (Integrada con JSON Database)
# ============================================================

from fastapi import FastAPI
from src.theaia.database.json_storage import JsonDatabaseManager
from src.theaia.database.config import DATABASE_PATH


# ============================================================
# 1️⃣ Inicializar la base de datos JSON
# ============================================================
# Crea una instancia de gestor JSON con la ruta definida en config.py
db = JsonDatabaseManager(DATABASE_PATH)


# ============================================================
# 2️⃣ Inicializar la aplicación FastAPI
# ============================================================

app = FastAPI(
    title="Thea IA API",
    description="Thea IA 3.0 — API básica con almacenamiento JSON",
    version="3.0.1",
)


# ============================================================
# 3️⃣ RUTAS DE VERIFICACIÓN Y OPERACIONES BÁSICAS
# ============================================================

@app.get("/health")
def health():
    """
    Endpoint para comprobar que la API está viva.
    """
    return {"status": "Thea IA API running successfully"}


@app.get("/notas")
def get_notas():
    """
    Devuelve todas las notas guardadas en la base JSON.
    """
    notas = db.get_all("notas")
    return {"total": len(notas), "data": notas}


@app.post("/notas/{nota_id}")
def create_nota(nota_id: str, titulo: str, contenido: str):
    """
    Crea una nueva nota (o sobrescribe la existente) en la base JSON.
    """
    nota = {"titulo": titulo, "contenido": contenido}
    db.insert("notas", nota_id, nota)
    return {"message": f"Nota {nota_id} guardada correctamente", "data": nota}


@app.get("/notas/{nota_id}")
def get_nota(nota_id: str):
    """
    Recupera una nota específica por su ID.
    """
    nota = db.get("notas", nota_id)
    if not nota:
        return {"error": f"No se encontró la nota {nota_id}"}
    return nota


@app.delete("/notas/{nota_id}")
def delete_nota(nota_id: str):
    """
    Elimina una nota por su ID.
    """
    if db.delete("notas", nota_id):
        return {"message": f"Nota {nota_id} eliminada correctamente"}
    return {"error": f"No existe la nota {nota_id}"}


# ============================================================
# ✅ Fin del archivo
# ============================================================

# Todas las partes de Telegram han sido eliminadas.
# Este código es completamente funcional con FastAPI + JSON DB.
