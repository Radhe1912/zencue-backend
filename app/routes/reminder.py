from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.reminder import Reminder
from app.models.user import User
from app.services.scheduler import add_job, remove_job

router = APIRouter(prefix="/reminders")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_reminder(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=data["user_id"]).first()

    reminder = Reminder(
        user_id=data["user_id"],
        cron_expression=data["cron_expression"],
        message=data.get("message"),
        reminder_type=data["reminder_type"],  # Ensure reminder_type is explicitly provided
        active=True
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    add_job(
        str(reminder.id),
        reminder.cron_expression,
        user.email,
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
        }
        for r in reminders
    ]
    
@router.post("/start/{id}")
def start_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()
    user = db.query(User).filter_by(id=reminder.user_id).first()

    reminder.active = True
    db.commit()

    add_job(
        str(reminder.id),
        reminder.cron_expression,
        user.email,
        reminder.message,
        reminder.reminder_type
    )

    return {"message": "Started"}

@router.post("/stop/{id}")
def stop_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()

    reminder.active = False
    db.commit()

    remove_job(str(id))

    return {"message": "Stopped"}

@router.delete("/{id}")
def delete_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter_by(id=id).first()

    remove_job(str(id))

    db.delete(reminder)
    db.commit()

    return {"message": "Deleted"}