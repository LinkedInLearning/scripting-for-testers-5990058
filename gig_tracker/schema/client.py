from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gig import Gig


class ClientBase(SQLModel):
    email_address: EmailStr
    first_name: str
    last_name: str
    phone_number: str  # TODO: Change to PhoneNumber
    address: str
    city: str
    province: str | None
    zip: str | None
    country: str | None


class Client(ClientBase, table=True):
    id: int = Field(default=None, primary_key=True)

    gigs: list["Gig"] = Relationship(back_populates="client")
    # todo: Add relationship to invoices
    # todo: Add communication log and relationship to it


class ClientCreate(ClientBase): ...


class ClientPublic(ClientBase):
    id: int
