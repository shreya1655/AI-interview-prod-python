from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Interview(Base):
    __tablename__ = "interviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    role: Mapped[str] = mapped_column(String(100))
    level: Mapped[str] = mapped_column(String(50))
    questions: Mapped[list] = mapped_column(JSON)
    answers: Mapped[list | None] = mapped_column(JSON, nullable=True)
    feedback: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="generated")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class ApiEvent(Base):
    __tablename__ = "api_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(120), index=True)
    event_type: Mapped[str] = mapped_column(String(40), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
