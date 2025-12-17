# ============================================================
# THEA IA 3.0 — MAIN API (Integrada con CoreOrchestrator)
# ============================================================

from fastapi import FastAPI, Body, HTTPException
from typing import Dict, Any
import asyncio

# --- Importaciones del Núcleo de Thea ---
# Importamos el orchestrator central que coordina todo
from theaia.core.orchestrator import CoreOrchestrator, OrchestratorResponse

# ============================================================
# 1️⃣ Inicializar el Núcleo de Thea IA
# ============================================================
# Creamos una única instancia del CoreOrchestrator al iniciar la app.
# Él se encargará de orquestar todos los agentes, conversaciones y el flujo.
try:
    orchestrator = CoreOrchestrator(language="es", session_timeout_minutes=30)
except Exception as e:
    # Si algo falla al cargar los componentes, la API no debe iniciar.
    raise RuntimeError(f"Error fatal al inicializar el CoreOrchestrator de Thea: {e}")


# ============================================================
# 2️⃣ Inicializar la aplicación FastAPI
# ============================================================
app = FastAPI(
    title="Thea IA API",
    description="Thea IA 3.0 — API conversacional orquestada por CoreOrchestrator.",
    version="3.0.2",
)


# ============================================================
# 3️⃣ RUTA PRINCIPAL DE INTERACCIÓN CON THEA
# ============================================================

@app.post("/chat/{user_id}")
async def handle_chat(user_id: str, payload: Dict[str, Any] = Body(...)):
    """
    Endpoint principal para procesar todos los mensajes del usuario.
    Recibe el mensaje y lo delega al CoreOrchestrator.
    """
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="El campo 'message' es obligatorio.")

    metadata = payload.get("metadata", {})

    # Llamamos al orchestrator para procesar el mensaje
    try:
        response: OrchestratorResponse = await orchestrator.process_message(
            user_id=user_id,
            message=message,
            metadata=metadata
        )
        
        return {
            "user_id": user_id,
            "response": response.message,
            "conversation_id": response.conversation_id,
            "state": response.state,
            "active_agent": response.active_agent,
            "intent": response.intent,
            "confidence": response.confidence,
            "context": response.context,
            "metadata": response.metadata,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")


# ============================================================
# 4️⃣ RUTA DE VERIFICACIÓN DE ESTADO
# ============================================================

@app.get("/health")
def health():
    """
    Endpoint para comprobar que la API y el núcleo de Thea están vivos.
    """
    return {
        "status": "Thea IA API running successfully",
        "version": "3.0.2",
        "orchestrator": "active"
    }


# ============================================================
# 5️⃣ RUTA DE AGENTES DISPONIBLES
# ============================================================

@app.get("/agents")
def get_agents():
    """
    Endpoint para obtener lista de agentes disponibles.
    """
    return {
        "agents": orchestrator.get_available_agents()
    }


# ============================================================
# 6️⃣ RUTA DE ESTADÍSTICAS
# ============================================================

@app.get("/stats")
def get_stats():
    """
    Endpoint para obtener estadísticas del orchestrator.
    """
    return orchestrator.get_stats()


# ============================================================
# ✅ Fin del archivo
# ============================================================
# Nota: Toda la lógica de negocio se gestiona a través del
# CoreOrchestrator que coordina agentes especializados.
# Mantiene una arquitectura limpia, escalable y centralizada.
