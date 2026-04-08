from pydantic import BaseModel
from uuid import UUID

class ReminderCreate(BaseModel):
    user_id: UUID
    cron_expression: str
    message: str

class ReminderResponse(BaseModel):
    id: UUID
    message: str
    active: bool

    class Config:
        from_attributes = True