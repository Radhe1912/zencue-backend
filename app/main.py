from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import app.models

from app.routes import auth, reminder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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