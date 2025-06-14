from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    purpose = Column(String, nullable=False)  # e.g. "consultation", "subscription"
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="success")

    user = relationship("User", backref="transactions")
