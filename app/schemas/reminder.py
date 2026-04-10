from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class ReminderCreate(BaseModel):
    user_id: UUID
    cron_expression: str
    message: Optional[str] = None
    reminder_type: str

class ReminderResponse(BaseModel):
    id: UUID
    message: str
    active: bool

    class Config:
        from_attributes = True