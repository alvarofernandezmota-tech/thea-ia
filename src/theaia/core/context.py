from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserContext(BaseModel):
    user_id: int
    state: Optional[str] = None
    last_message: Optional[str] = None
    last_response: Optional[str] = None
    data: Dict[str, Any] = {}
