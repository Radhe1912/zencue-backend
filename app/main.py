from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.services.scheduler import scheduler
from app.core.database import SessionLocal
from app.models.reminder import Reminder
from app.services.scheduler import add_job

from app.routes import auth, push, reminder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://zencue.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(push.router)
app.include_router(reminder.router)


@app.get("/")
def home():
    return {"message": "ZenCue running"}

@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()

    db = SessionLocal()
    try:
        reminders = db.query(Reminder).filter(Reminder.active == True).all()
        for reminder in reminders:
            add_job(
                str(reminder.id),
                reminder.cron_expression,
                reminder.user_id,
                reminder.message,
                reminder.reminder_type,
            )
    finally:
        db.close()
