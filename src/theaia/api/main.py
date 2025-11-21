# ======================================================
# THEA IA — API con FastAPI + PostgreSQL
# ======================================================
# Versión: 3.1.0 (H03 AgendaAgent Integration)
# Status: Production-Ready
# ======================================================

from fastapi import FastAPI, HTTPException
from typing import Dict, Any

# Import AgendaAgent router
from src.theaia.api.endpoints.agenda import router as agenda_router

# Crear instancia FastAPI
app = FastAPI(
    title="THEA IA API",
    description="API REST para THEA IA - Sistema Conversacional Multi-Agent",
    version="3.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ======================================================
# INCLUDE ROUTERS
# ======================================================
app.include_router(agenda_router)  # AgendaAgent endpoints

# ======================================================
# HEALTH CHECK ENDPOINT
# ======================================================
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:  # ✅ CAMBIADO: str → Any
    """
    Health check endpoint para monitoreo y deployment.
    
    Returns:
        Dict con status si API está operativa
    """
    return {
        "status": "healthy",
        "version": "3.1.0",
        "agents": ["agenda"]  # ✅ Ahora acepta lista
    }

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
        "version": "3.1.0",
        "status": "active",
        "agents": {
            "agenda": "/agents/agenda"
        },
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "agenda_health": "/agents/agenda/health",
            "create_event": "/agents/agenda/create-event",
            "list_events": "/agents/agenda/events"
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
    print("✅ THEA IA API iniciada - v3.1.0")
    print("🤖 AgendaAgent API: /agents/agenda")
    print("📝 Docs: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown():
    """Limpieza al apagar la API."""
    print("🛑 THEA IA API apagada")
