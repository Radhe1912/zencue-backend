import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.models.otp import OTP
from app.services.email_service import send_email
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-otp")
def send_otp(email: str, db: Session = Depends(get_db)):
    otp_code = str(random.randint(100000, 999999))

    db.query(OTP).filter(OTP.email == email).delete()

    new_otp = OTP(email=email, otp=otp_code)

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    send_email(email, f"Your OTP is {otp_code}")

    return {"message": "OTP sent"}

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, password: str, db: Session = Depends(get_db)):
    record = db.query(OTP).filter_by(email=email, otp=otp).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    db.delete(record)

    user = User(
        email=email,
        password=hash_password(password),
        is_verified=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created",
        "user_id": str(user.id)
    }

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(password, user.password):
        return {"error": "Wrong password"}

    return {
        "message": "Login success",
        "user_id": str(user.id)
    }