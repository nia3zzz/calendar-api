from ..db.engine import base
from sqlalchemy import String, DateTime, func, UUID, String
from uuid import uuid4
from sqlalchemy.orm import Mapped, relationship, mapped_column
import datetime
from .event_model import Event


# defining the user model
class User(base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, insert_default=uuid4, index=True)

    first_name: Mapped[str] = mapped_column(String(30))

    last_name: Mapped[str] = mapped_column(String(30), nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    profile_picture: Mapped[str] = mapped_column(
        String(500),
        insert_default="https://www.shutterstock.com/image-vector/default-avatar-profile-icon-social-600nw-1677509740.jpg",
        nullable=False,
    )

    password: Mapped[str] = mapped_column(String(300), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    events: Mapped[list["Event"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
