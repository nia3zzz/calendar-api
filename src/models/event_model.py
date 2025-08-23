from typing import TYPE_CHECKING
from db.engine import base
from uuid import uuid4, UUID
from sqlalchemy import ForeignKey, String, DateTime, JSON, Boolean, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime


# to avoid circular imports
if TYPE_CHECKING:
    from .user_model import User


# defining the event model
class Event(base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, index=True)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    description: Mapped[str] = mapped_column(String, nullable=False)

    roles: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)

    is_recurring: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    recurrence_rule: Mapped[str] = mapped_column(String, nullable=False, default=None)

    start_timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    end_timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    recurrence_end_timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=True, default=None
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="events")

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, user_id={self.user_id!r})"
