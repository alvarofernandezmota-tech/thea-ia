import json
from pathlib import Path
from theaia.core.context import UserContext

# Directorio local para contextos (puede adaptarse a base de datos más adelante)
CONTEXT_DIR = Path("data/contexts")
CONTEXT_DIR.mkdir(parents=True, exist_ok=True)

def _context_file(user_id: int) -> Path:
    return CONTEXT_DIR / f"context_{user_id}.json"

def load_context(user_id: int) -> UserContext:
    """
    Carga el contexto de usuario desde un archivo JSON.
    Si no existe, devuelve contexto vacío.
    """
    path = _context_file(user_id)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return UserContext(**data)
    return UserContext(user_id=user_id)

def save_context(ctx: UserContext) -> None:
    """
    Persiste el contexto de usuario en un archivo JSON.
    """
    path = _context_file(ctx.user_id)
    with path.open("w", encoding="utf-8") as f:
        f.write(ctx.json())
