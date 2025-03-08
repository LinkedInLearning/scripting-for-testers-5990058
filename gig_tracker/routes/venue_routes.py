from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..schema.base import get_session
from ..schema.venue import Venue, VenueCreate, VenuePublic

SessionDep = Annotated[Session, Depends(get_session)]
venue_router = APIRouter(prefix="/api")


@venue_router.post("/venues", response_model=VenuePublic, status_code=201)
def create_venue(venue: VenueCreate, session: SessionDep):
    db_venue = Venue.model_validate(venue)

    session.add(db_venue)
    session.commit()
    session.refresh(db_venue)

    return db_venue


@venue_router.get("/venues", response_model=list[VenuePublic])
def get_venues(session: SessionDep):
    venues = session.exec(select(Venue)).all()

    return list(venues)


@venue_router.get("/venues/{venue_id}", response_model=VenuePublic)
def get_venue(venue_id: int, session: SessionDep):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    return venue


@venue_router.put("/venues/{venue_id}", response_model=VenuePublic)
def update_venue(venue_id: int, venue: VenueCreate, session: SessionDep):
    db_venue = session.get(Venue, venue_id)
    if not db_venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    venue_data = venue.model_dump(exclude_unset=True)
    db_venue.sqlmodel_update(venue_data)
    session.add(db_venue)
    session.commit()
    session.refresh(db_venue)

    return db_venue


@venue_router.delete("/venues/{venue_id}", status_code=204)
def delete_venue(venue_id: int, session: SessionDep):
    venue = session.get(Venue, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")

    session.delete(venue)
    session.commit()

    return Response(status_code=204)
