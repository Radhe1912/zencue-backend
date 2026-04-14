from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.push_subscription import PushSubscription
from app.models.user import User
from app.schemas.push import PushSubscriptionCreate, PushSubscriptionDelete
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
        else:
            # Direct format { user_id, endpoint, keys: {...} }
            endpoint = data.get("endpoint")
            keys = data.get("keys", {})
        
        if not endpoint or not keys.get("p256dh") or not keys.get("auth"):
            raise ValueError("Missing required subscription fields")
        
        # Check if subscription already exists
        existing = db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id,
            PushSubscription.endpoint == endpoint
        ).first()
        
        if existing:
            existing.active = True
            db.commit()
            return {"message": "Subscription updated"}
        
        push_subscription = PushSubscription(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=keys.get("p256dh"),
            auth=keys.get("auth"),
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


@router.post("/subscribe")
def subscribe(payload: PushSubscriptionCreate, db: Session = Depends(get_db)):
    if not is_push_configured():
        raise HTTPException(status_code=503, detail="Web push is not configured.")

    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    subscription_data = payload.subscription
    existing = (
        db.query(PushSubscription)
        .filter(PushSubscription.endpoint == subscription_data.endpoint)
        .first()
    )

    if existing:
        existing.user_id = payload.user_id
        existing.p256dh = subscription_data.keys.p256dh
        existing.auth = subscription_data.keys.auth
        existing.expiration_time = subscription_data.expirationTime
        existing.user_agent = payload.user_agent
        existing.active = True
    else:
        existing = PushSubscription(
            user_id=payload.user_id,
            endpoint=subscription_data.endpoint,
            p256dh=subscription_data.keys.p256dh,
            auth=subscription_data.keys.auth,
            expiration_time=subscription_data.expirationTime,
            user_agent=payload.user_agent,
            active=True,
        )
        db.add(existing)

    db.commit()
    return {"message": "Push notifications enabled."}


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
