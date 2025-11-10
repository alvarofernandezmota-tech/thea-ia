# ======================================================
# THEA IA — API BÁSICA con FastAPI + Base de Datos JSON
# ======================================================
# Versión: 3.0.2 (S39-AUDIT Enhanced)
# Status: Production-Ready
# ======================================================

from fastapi import FastAPI, HTTPException, Query
from typing import Optional, Dict, Any
from src.theaia.database.json_storage import JsonDatabaseManager
from src.theaia.database.config import DATABASE_PATH


# Inicializar base JSON
db = JsonDatabaseManager(DATABASE_PATH)


# Crear instancia FastAPI
app = FastAPI(
    title="THEA IA API",
    description="API REST para THEA IA - Sistema Conversacional con almacenamiento JSON",
    version="3.0.2",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ======================================================
# HEALTH CHECK ENDPOINT
# ======================================================
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint para monitoreo y deployment (Render, Docker).
    
    Returns:
        Dict con status: "ok" si API está operativa
    """
    return {
        "status": "THEA IA API running successfully",
        "version": "3.0.2"
    }


# ======================================================
# NOTAS ENDPOINTS — CRUD COMPLETO
# ======================================================

@app.get("/notas", tags=["Notes"])
async def get_notas(limit: Optional[int] = Query(None, ge=1, le=100)) -> Dict[str, Any]:
    """
    Obtiene todas las notas almacenadas.
    
    Query Parameters:
        limit (int, optional): Limita cantidad de resultados (1-100)
    
    Returns:
        Dict con total de notas y lista de datos
    
    Example:
        GET /notas
        GET /notas?limit=10
    """
    try:
        notas = db.get_all("notas")
        if limit:
            notas = notas[:limit]
        return {
            "total": len(notas),
            "data": notas,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener notas: {str(e)}")


@app.post("/notas/{id}", tags=["Notes"])
async def create_nota(
    id: str,
    titulo: str = Query(..., min_length=1, max_length=200),
    contenido: str = Query(..., min_length=1, max_length=5000)
) -> Dict[str, Any]:
    """
    Crea una nueva nota.
    
    Parameters:
        id (str): Identificador único de la nota
        titulo (str): Título de la nota (1-200 caracteres)
        contenido (str): Contenido de la nota (1-5000 caracteres)
    
    Returns:
        Dict con mensaje de éxito y datos guardados
    
    Example:
        POST /notas/nota_001?titulo=Mi Nota&contenido=Contenido importante
    """
    try:
        if not id or not id.strip():
            raise HTTPException(status_code=400, detail="ID no puede estar vacío")
        
        nueva = {
            "titulo": titulo.strip(),
            "contenido": contenido.strip()
        }
        db.insert("notas", id, nueva)
        return {
            "status": "success",
            "message": f"Nota '{id}' guardada correctamente",
            "data": nueva
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear nota: {str(e)}")


@app.get("/notas/{id}", tags=["Notes"])
async def get_nota(id: str) -> Dict[str, Any]:
    """
    Obtiene una nota específica por ID.
    
    Parameters:
        id (str): Identificador de la nota
    
    Returns:
        Dict con datos de la nota
    
    Raises:
        HTTPException: 404 si la nota no existe
    
    Example:
        GET /notas/nota_001
    """
    try:
        nota = db.get("notas", id)
        if not nota:
            raise HTTPException(
                status_code=404,
                detail=f"Nota '{id}' no encontrada"
            )
        return {
            "status": "success",
            "data": nota,
            "id": id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener nota: {str(e)}")


@app.delete("/notas/{id}", tags=["Notes"])
async def delete_nota(id: str) -> Dict[str, Any]:
    """
    Elimina una nota específica.
    
    Parameters:
        id (str): Identificador de la nota
    
    Returns:
        Dict con mensaje de éxito
    
    Raises:
        HTTPException: 404 si la nota no existe
    
    Example:
        DELETE /notas/nota_001
    """
    try:
        if db.delete("notas", id):
            return {
                "status": "success",
                "message": f"Nota '{id}' eliminada correctamente"
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Nota '{id}' no existe"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar nota: {str(e)}")


# ======================================================
# ROOT ENDPOINT
# ======================================================
@app.get("/", tags=["Info"])
async def root() -> Dict[str, Any]:
    """
    Endpoint raíz con información de la API.
    """
    return {
        "name": "THEA IA API",
        "version": "3.0.2",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "notes": "/notas"
        }
    }


# ======================================================
# ERROR HANDLERS
# ======================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado para excepciones HTTP."""
    return {
        "status": "error",
        "detail": exc.detail,
        "status_code": exc.status_code
    }


# ======================================================
# STARTUP & SHUTDOWN
# ======================================================
@app.on_event("startup")
async def startup():
    """Inicialización al arrancar la API."""
    print("✅ THEA IA API iniciada - v3.0.2")
    print(f"📁 Base de datos: {DATABASE_PATH}")


@app.on_event("shutdown")
async def shutdown():
    """Limpieza al apagar la API."""
    print("🛑 THEA IA API apagada")