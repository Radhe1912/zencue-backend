from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import app.models
from app.services.scheduler import scheduler

from app.routes import auth, reminder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://zencue.vercel.app/", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(reminder.router)


@app.get("/")
def home():
    return {"message": "ZenCue running"}

@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()