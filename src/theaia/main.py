# ============================================================
# THEA IA 3.0 — MAIN API (Integrada con CoreManager)
# ============================================================

from fastapi import FastAPI, Body, HTTPException
from typing import Dict, Any

# --- Importaciones del Núcleo de Thea ---
# Ahora importamos el cerebro central: CoreManager
from src.theaia.core.manager import CoreManager

# ============================================================
# 1️⃣ Inicializar el Núcleo de Thea IA
# ============================================================
# Creamos una única instancia del CoreManager al iniciar la app.
# Él se encargará de inicializar el router, los agentes, la FSM y la DB.
try:
    core_logic = CoreManager()
except Exception as e:
    # Si algo falla al cargar los modelos o agentes, la API no debe iniciar.
    raise RuntimeError(f"Error fatal al inicializar el CoreManager de Thea: {e}")


# ============================================================
# 2️⃣ Inicializar la aplicación FastAPI
# ============================================================
app = FastAPI(
    title="Thea IA API",
    description="Thea IA 3.0 — API conversacional orquestada por CoreManager.",
    version="3.0.2",
)


# ============================================================
# 3️⃣ RUTA PRINCIPAL DE INTERACCIÓN CON THEA
# ============================================================

@app.post("/chat/{user_id}")
async def handle_chat(user_id: str, payload: Dict[str, Any] = Body(...)):
    """
    Endpoint principal para procesar todos los mensajes del usuario.
    Recibe el mensaje, el estado actual y el contexto, y los delega al CoreManager.
    """
    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="El campo 'message' es obligatorio.")

    state = payload.get("state", "initial")
    context = payload.get("context", {})

    # Llamamos al manejador central del núcleo de Thea.
    # Toda la inteligencia (FSM, Router, Agentes) se ejecuta aquí.
    response, new_state, new_context = core_logic.handle(
        user_id=user_id,
        message=message,
        state=state,
        context=context
    )

    return {
        "user_id": user_id,
        "response": response,
        "state": new_state,
        "context": new_context,
    }


# ============================================================
# 4️⃣ RUTA DE VERIFICACIÓN DE ESTADO
# ============================================================

@app.get("/health")
def health():
    """
    Endpoint para comprobar que la API y el núcleo de Thea están vivos.
    """
    return {"status": "Thea IA API running successfully"}

# ============================================================
# ✅ Fin del archivo
# ============================================================
# Nota: Las rutas directas a /notas (/get_notas, /create_nota, etc.)
# han sido eliminadas. Ahora toda la lógica de negocio se gestiona
# a través de los agentes (como NoteAgent) y se centraliza en el
# endpoint único /chat para mantener una arquitectura limpia y escalable.
