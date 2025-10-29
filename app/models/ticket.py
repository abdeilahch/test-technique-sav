import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.sqlite import INTEGER
from app.db.base import Base
import enum


class TicketStatus(str, enum.Enum):
    open = "open"
    stalled = "stalled"
    closed = "closed"

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.open, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
