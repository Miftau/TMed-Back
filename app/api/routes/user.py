from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.user import UserOut
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
