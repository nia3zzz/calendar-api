import strawberry
from uuid import UUID
import datetime
import typing
from .event_schema import Event


@strawberry.type
class User:
    id: UUID
    first_name: str
    last_name: str
    email: str
    profile_picture: str
    password: str
    created_At: datetime.datetime
    updated_At: datetime.datetime
    events: typing.List[Event]
