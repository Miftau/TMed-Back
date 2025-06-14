from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserOut


class PatientBase(BaseModel):
    medical_history: Optional[str] = None
    address: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    id: int
    user: UserOut

    class Config:
        orm_mode = True
