import random
from datetime import datetime, timedelta
from uuid import UUID
from app.services.email_service import send_otp_email

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.models.user import User
from app.models.otp import OTP
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
    user = db.query(User).filter_by(email=email).first()

    if user and user.is_verified:
        return {
            "is_existing": True,
            "message": "Account found. Please sign in with your password."
        }

    otp_code = str(random.randint(100000, 999999))

    db.query(OTP).filter(OTP.email == email).delete()

    new_otp = OTP(
        email=email,
        otp=otp_code
    )

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    email_sent = send_otp_email(email, otp_code)

    if not email_sent:
        db.delete(new_otp)
        db.commit()
        raise HTTPException(
            status_code=503,
            detail="OTP delivery is unavailable on this deployment right now. Existing users can still sign in with password."
        )

    return {
        "is_existing": False,
        "message": "Verification code sent. Complete setup to create your account."
    }

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, password: str, db: Session = Depends(get_db)):
    record = db.query(OTP).filter_by(email=email, otp=otp).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    db.delete(record)

    user = db.query(User).filter_by(email=email).first()

    if user:
        user.password = hash_password(password)
        user.is_verified = True

        db.commit()
        db.refresh(user)

        return {
            "message": "User updated",
            "user_id": str(user.id)
        }

    try:
        new_user = User(
            email=email,
            password=hash_password(password),
            is_verified=True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User created",
            "user_id": str(new_user.id)
        }

    except IntegrityError:
        db.rollback()

        user = db.query(User).filter_by(email=email).first()

        if user:
            user.password = hash_password(password)
            user.is_verified = True

            db.commit()
            db.refresh(user)

            return {
                "message": "User updated (fallback)",
                "user_id": str(user.id)
            }

        raise HTTPException(status_code=500, detail="User creation failed")

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.password:
        raise HTTPException(status_code=400, detail="User not verified")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    return {
        "message": "Login success",
        "user_id": str(user.id)
    }


@router.get("/session/{user_id}")
def get_session(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_verified:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "user_id": str(user.id),
        "email": user.email,
        "is_verified": user.is_verified,
    }
