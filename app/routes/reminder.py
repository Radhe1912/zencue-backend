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
    user_id = data.get("user_id")
    cron = data.get("cron_expression")
    message = data.get("message")

    # 🔍 get user email
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    reminder = Reminder(
        user_id=user_id,
        cron_expression=cron,
        message=message,
        active=True
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    # ✅ schedule job
    add_job(str(reminder.id), cron, user.email, message)

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
        }
        for r in reminders
    ]
    
@router.post("/stop/{id}")
def stop_reminder(id: UUID, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == id).first()

    if reminder:
        reminder.active = False
        db.commit()
        remove_job(str(id))

    return {"status": "stopped"}