from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.push_subscription import PushSubscription
from app.models.reminder import Reminder
from app.models.user import User
from app.schemas.reminder import ReminderCreate
from app.services.scheduler import add_job, remove_job

router = APIRouter(prefix="/reminders")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_push_enabled(db: Session, user_id: UUID):
    subscription = (
        db.query(PushSubscription)
        .filter(
            PushSubscription.user_id == user_id,
            PushSubscription.active.is_(True),
        )
        .first()
    )
    if not subscription:
        raise HTTPException(
            status_code=400,
            detail="Enable browser notifications on this device before creating reminders.",
        )


@router.post("/")
def create_reminder(data: ReminderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    ensure_push_enabled(db, data.user_id)

    reminder = Reminder(
        user_id=data.user_id,
        cron_expression=data.cron_expression,
        message=data.message,
        reminder_type=data.reminder_type,
        active=True,
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    add_job(
        str(reminder.id),
        reminder.cron_expression,
        reminder.user_id,
        reminder.message,
        reminder.reminder_type
    )

    return {"message": "Reminder created"}

@router.get("/user/{user_id}")
def get_user_reminders(user_id: UUID, db: Session = Depends(get_db)):
    reminders = db.query(Reminder).filter(Reminder.user_id == user_id).all()

    return [
        {
            "id": str(r.id),
            "message": r.message,
            "cron_expression": r.cron_expression,
            "active": r.active,
            "reminder_type": r.reminder_type,
            "user_id": str(r.user_id),
        }
        for r in reminders
    ]
    
@router.post("/start/{id}")
def start_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found.")

    ensure_push_enabled(db, reminder.user_id)

    reminder.active = True
    db.commit()

    add_job(
        str(reminder.id),
        reminder.cron_expression,
        reminder.user_id,
        reminder.message,
        reminder.reminder_type
    )

    return {"message": "Started"}

@router.post("/stop/{id}")
def stop_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found.")

    reminder.active = False
    db.commit()

    remove_job(str(id))

    return {"message": "Stopped"}

@router.delete("/{id}")
def delete_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found.")

    remove_job(str(id))

    db.delete(reminder)
    db.commit()

    return {"message": "Deleted"}

@router.post("/push/subscribe")
def subscribe(data: dict, db: Session = Depends(get_db)):
    subscription = PushSubscription(
        user_id=data["user_id"],
        endpoint=data["endpoint"],
        p256dh=data["keys"]["p256dh"],
        auth=data["keys"]["auth"],
        active=True
    )

    db.add(subscription)
    db.commit()

    return {"message": "Subscribed"}
