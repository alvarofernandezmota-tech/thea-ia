from src.theaia.database.connections import Session
from src.theaia.database.models import UserContext

def save_context(user_id: str, state: str, data: dict) -> None:
    session = Session()
    try:
        ctx = session.query(UserContext).get(user_id)
        if ctx:
            ctx.state = state
            ctx.data = data
        else:
            ctx = UserContext(user_id=user_id, state=state, data=data)
            session.add(ctx)
        session.commit()
    finally:
        session.close()

def load_context(user_id: str) -> dict | None:
    session = Session()
    try:
        ctx = session.query(UserContext).get(user_id)
        if ctx:
            return {"user_id": ctx.user_id, "state": ctx.state, "data": ctx.data}
        return None
    finally:
        session.close()

def update_context(user_id: str, updates: dict) -> None:
    session = Session()
    try:
        ctx = session.query(UserContext).get(user_id)
        if ctx:
            for k, v in updates.items():
                setattr(ctx, k, v)
            session.commit()
    finally:
        session.close()
