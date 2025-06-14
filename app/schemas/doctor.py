from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserOut


class DoctorBase(BaseModel):
    specialization: str
    bio: Optional[str] = None
    location: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorOut(DoctorBase):
    id: int
    user: UserOut

    class Config:
        orm_mode = True
