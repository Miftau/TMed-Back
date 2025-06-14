from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class AppointmentType(str, Enum):
    online = "online"
    home_visit = "home_visit"


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_time: datetime
    type: AppointmentType
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    status: AppointmentStatus

    class Config:
        orm_mode = True
