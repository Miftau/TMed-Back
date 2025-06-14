from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
