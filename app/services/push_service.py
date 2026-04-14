import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.models.push_subscription import PushSubscription


try:
    from pywebpush import WebPushException, webpush
except ImportError:  # pragma: no cover - handled at runtime when dependency is missing
    WebPushException = Exception
    webpush = None


BACKEND_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(BACKEND_ENV_PATH)

APP_URL = os.getenv("APP_URL", "https://zencue.vercel.app").rstrip("/")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT", f"{APP_URL}/contact")

PUSH_THEMES = {
    "water": {"title": "Hydration reset", "tag": "zencue-water"},
    "posture": {"title": "Posture reset", "tag": "zencue-posture"},
    "motivation": {"title": "Momentum boost", "tag": "zencue-motivation"},
    "custom": {"title": "ZenCue reminder", "tag": "zencue-custom"},
}


def is_push_configured() -> bool:
    return bool(webpush and VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY)


def get_vapid_public_key() -> str | None:
    return VAPID_PUBLIC_KEY


def get_dashboard_url() -> str:
    return APP_URL if "#/" in APP_URL else f"{APP_URL}/#/dashboard"


def build_subscription_info(subscription: PushSubscription) -> dict:
    return {
        "endpoint": subscription.endpoint,
        "expirationTime": subscription.expiration_time,
        "keys": {
            "p256dh": subscription.p256dh,
            "auth": subscription.auth,
        },
    }


def build_payload(message: str, reminder_type: str = "custom") -> dict:
    theme = PUSH_THEMES.get(reminder_type, PUSH_THEMES["custom"])
    asset_url = f"{APP_URL}/favicon.svg"

    return {
        "title": theme["title"],
        "body": message,
        "tag": theme["tag"],
        "icon": asset_url,
        "badge": asset_url,
        "data": {
            "url": get_dashboard_url(),
            "reminder_type": reminder_type,
        },
    }


def send_push_notification(subscription: PushSubscription, payload: dict) -> None:
    if not is_push_configured():
        raise RuntimeError("Web push is not configured.")

    webpush(
        subscription_info=build_subscription_info(subscription),
        data=json.dumps(payload),
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims={"sub": VAPID_SUBJECT},
        ttl=60,
    )


def send_push_to_user(db: Session, user_id, message: str, reminder_type: str = "custom") -> int:
    subscriptions = (
        db.query(PushSubscription)
        .filter(
            PushSubscription.user_id == user_id,
            PushSubscription.active.is_(True),
        )
        .all()
    )

    if not subscriptions or not is_push_configured():
        return 0

    payload = build_payload(message, reminder_type)
    stale_ids = []
    delivered = 0

    for subscription in subscriptions:
        try:
            send_push_notification(subscription, payload)
            delivered += 1
        except WebPushException as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            print(f"Push delivery failed for {subscription.endpoint}: {exc}")
            if status_code in {404, 410}:
                stale_ids.append(subscription.id)
        except Exception as exc:
            print(f"Push delivery failed for {subscription.endpoint}: {exc}")

    if stale_ids:
        (
            db.query(PushSubscription)
            .filter(PushSubscription.id.in_(stale_ids))
            .delete(synchronize_session=False)
        )
        db.commit()

    return delivered
