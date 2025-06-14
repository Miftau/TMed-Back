from pydantic import BaseModel
from datetime import datetime


class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    record: str


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordOut(MedicalRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
