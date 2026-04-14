from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscriptionPayload(BaseModel):
    endpoint: str
    expirationTime: Optional[int] = None
    keys: PushSubscriptionKeys


class PushSubscriptionCreate(BaseModel):
    user_id: UUID
    subscription: PushSubscriptionPayload
    user_agent: Optional[str] = None


class PushSubscriptionDelete(BaseModel):
    user_id: UUID
    endpoint: str
