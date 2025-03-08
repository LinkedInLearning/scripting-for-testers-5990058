from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gig import Gig


class VenueBase(SQLModel):
    name: str
    address: str
    contact_number: str | None = None
    contact_email: str | None = None
    capacity: int | None = None
    notes: str | None = None


class Venue(VenueBase, table=True):
    id: int = Field(default=None, primary_key=True)

    gigs: list["Gig"] = Relationship(back_populates="venue")


class VenueCreate(VenueBase): ...


class VenuePublic(VenueBase):
    id: int


class Venues(SQLModel):
    venues: list[Venue]
