from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.push_subscription import PushSubscription
from app.schemas.push import PushSubscriptionDelete
from app.services.push_service import get_vapid_public_key, is_push_configured

router = APIRouter(prefix="/push")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/vapid-public-key")
def get_public_key():
    public_key = get_vapid_public_key()
    if not public_key or not is_push_configured():
        raise HTTPException(status_code=503, detail="Web push is not configured.")

    return {"public_key": public_key}


@router.get("/public_key")
def get_public_key_alias():
    public_key = get_vapid_public_key()
    if not public_key or not is_push_configured():
        raise HTTPException(status_code=503, detail="Web push is not configured.")

    return {"publicKey": public_key}


@router.post("/subscribe")
def subscribe_to_push(data: dict, db: Session = Depends(get_db)):
    try:
        user_id = data.get("user_id")

        # Handle both subscription formats
        if "subscription" in data:
            # Frontend sends { user_id, subscription: {...}, user_agent: "..." }
            subscription = data.get("subscription", {})
            endpoint = subscription.get("endpoint")
            keys = subscription.get("keys", {})
            user_agent = data.get("user_agent")
            expiration_time = subscription.get("expirationTime")
        else:
            # Direct format { user_id, endpoint, keys: {...} }
            endpoint = data.get("endpoint")
            keys = data.get("keys", {})
            user_agent = data.get("user_agent")
            expiration_time = data.get("expirationTime")

        if not endpoint or not keys.get("p256dh") or not keys.get("auth"):
            raise ValueError("Missing required subscription fields")

        # Check if subscription already exists
        existing = db.query(PushSubscription).filter(
            PushSubscription.endpoint == endpoint
        ).first()

        if existing:
            existing.user_id = user_id
            existing.p256dh = keys.get("p256dh")
            existing.auth = keys.get("auth")
            existing.expiration_time = expiration_time
            existing.user_agent = user_agent
            existing.active = True
            db.commit()
            return {"message": "Subscription updated"}

        push_subscription = PushSubscription(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=keys.get("p256dh"),
            auth=keys.get("auth"),
            expiration_time=expiration_time,
            user_agent=user_agent,
            active=True,
        )

        db.add(push_subscription)
        db.commit()

        return {"message": "Subscribed successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status/{user_id}")
def get_push_status(user_id: UUID, db: Session = Depends(get_db)):
    count = (
        db.query(PushSubscription)
        .filter(
            PushSubscription.user_id == user_id,
            PushSubscription.active.is_(True),
        )
        .count()
    )

    return {
        "configured": is_push_configured(),
        "enabled": count > 0,
        "subscription_count": count,
    }


@router.post("/unsubscribe")
def unsubscribe(payload: PushSubscriptionDelete, db: Session = Depends(get_db)):
    subscription = (
        db.query(PushSubscription)
        .filter(
            PushSubscription.user_id == payload.user_id,
            PushSubscription.endpoint == payload.endpoint,
        )
        .first()
    )

    if subscription:
        db.delete(subscription)
        db.commit()

    return {"message": "Push notifications disabled."}
