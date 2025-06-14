from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    user_id: int
    amount: float
    purpose: str


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True
