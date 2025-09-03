import strawberry
from uuid import UUID
import datetime
from .user_schema import User
import typing
import enum


class RoleEnum(enum.Enum):
    VIEWER = "viewer"
    EDITOR = "editor"


@strawberry.type
class EventRole:
    id: UUID
    user: User
    role: RoleEnum


@strawberry.type
class Event:
    id: UUID
    description: str
    roles: typing.List[EventRole]
    is_recurring: bool
    recurrence_rule: str
    start_timestamp: datetime.datetime
    end_timestamp: datetime.datetime
    recurrence_end_timestamp: datetime.datetime
    created_At: datetime.datetime
    updated_At: datetime.datetime
    user: User
