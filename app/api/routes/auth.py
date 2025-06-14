from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.models.patient import Patient
from app.models.doctor import Doctor


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if existing := db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed_password,
        phone=user_in.phone,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == UserRole.patient:
        patient = Patient(user_id=user.id)
        db.add(patient)
    elif user.role == UserRole.doctor:
        doctor = Doctor(user_id=user.id)
        db.add(doctor)

    db.commit()

    return user



@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
