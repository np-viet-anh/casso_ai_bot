from typing import Any, Dict
from pydantic import BaseModel

class TelegramUpdate(BaseModel):
    update_id: int
    message: Dict[str, Any] | None = None
    callback_query: Dict[str, Any] | None = None

class MockPayOsPayload(BaseModel):
    order_id: str
    description: str
