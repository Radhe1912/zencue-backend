from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import AuthRequest
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def normalize_email(raw_email: str) -> str:
    email = raw_email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    return email


def validate_password(password: str) -> str:
    cleaned_password = password.strip()
    if len(cleaned_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    return cleaned_password


@router.post("/register")
def register(payload: AuthRequest, db: Session = Depends(get_db)):
    email = normalize_email(payload.email)
    password = validate_password(payload.password)

    user = db.query(User).filter_by(email=email).first()

    if user and user.password:
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    if user:
        user.password = hash_password(password)
        user.is_verified = True
        db.commit()
        db.refresh(user)
        return {
            "message": "Account ready",
            "user_id": str(user.id)
        }

    new_user = User(
        email=email,
        password=hash_password(password),
        is_verified=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account created",
        "user_id": str(new_user.id)
    }

@router.post("/login")
def login(payload: AuthRequest, db: Session = Depends(get_db)):
    email = normalize_email(payload.email)
    password = validate_password(payload.password)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not user.password:
        raise HTTPException(status_code=400, detail="This account needs a password. Create it first.")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password.")

    if not user.is_verified:
        user.is_verified = True
        db.commit()

    return {
        "message": "Login success",
        "user_id": str(user.id)
    }


@router.get("/session/{user_id}")
def get_session(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.password:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "user_id": str(user.id),
        "email": user.email,
        "is_verified": user.is_verified,
    }
