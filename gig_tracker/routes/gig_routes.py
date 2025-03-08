from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select

from ..rate_limiter import limiter
from ..schema.base import get_session
from ..schema.gig import Gig, GigCreate, GigPublic

SessionDep = Annotated[Session, Depends(get_session)]
gig_router = APIRouter(prefix="/api")


@gig_router.post("/gigs", response_model=GigPublic, status_code=201)
@limiter.limit("5/minute")
def create_gig(request: Request, gig: GigCreate, session: SessionDep):
    db_gig = Gig.model_validate(gig)

    session.add(db_gig)
    session.commit()
    session.refresh(db_gig)

    return db_gig


@gig_router.get("/gigs", response_model=list[GigPublic])
@limiter.limit("2/second")
def get_gigs(request: Request, session: SessionDep):
    gigs = session.exec(select(Gig)).all()

    return list(gigs)


@gig_router.put("/gigs/{gig_id}", response_model=GigPublic)
@limiter.limit("10/minute")
def update_gig(request: Request, gig_id: int, gig: GigCreate, session: SessionDep):
    db_gig = session.get(Gig, gig_id)
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    gig_data = gig.model_dump(exclude_unset=True)
    db_gig.sqlmodel_update(gig_data)
    session.add(db_gig)
    session.commit()
    session.refresh(db_gig)

    return db_gig


@gig_router.delete("/gigs/{gig_id}", status_code=204)
@limiter.limit("4/minute")
def delete_gig(request: Request, gig_id: int, session: SessionDep):
    gig = session.get(Gig, gig_id)
    if not gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    session.delete(gig)
    session.commit()

    return Response(status_code=204)
