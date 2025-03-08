from datetime import date, time

from sqlmodel import Field, Relationship, SQLModel

from ..schema.client import Client
from ..schema.venue import Venue


class GigBase(SQLModel):
    date: date
    time: time
    name: str


class Gig(GigBase, table=True):
    id: int = Field(default=None, primary_key=True)

    venue_id: int = Field(default=None, foreign_key="venue.id")
    venue: Venue = Relationship(back_populates="gigs")

    client_id: int = Field(default=None, foreign_key="client.id")
    client: Client = Relationship(back_populates="gigs")


class GigCreate(GigBase):
    venue_id: int
    client_id: int


class GigPublic(GigBase):
    id: int
    venue_id: int
    client_id: int


class Gigs(SQLModel):
    gigs: list[Gig]
