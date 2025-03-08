from datetime import date, time
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from jinja2_fragments.fastapi import Jinja2Blocks
from sqlmodel import Session, col, select

from ..schema.base import get_session
from ..schema.client import Client
from ..schema.gig import Gig
from ..schema.venue import Venue

ui_router = APIRouter()

templates = Jinja2Blocks(directory="./templates")
SessionDep = Annotated[Session, Depends(get_session)]


@ui_router.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@ui_router.get("/gigs", include_in_schema=False)
def gigs(request: Request, session: SessionDep):
    result = session.exec(select(Gig).where(Gig.date >= date.today())).all()

    return templates.TemplateResponse("gigs.html", {"request": request, "gigs": result})


@ui_router.get("/clients", include_in_schema=False)
def get_clients(request: Request, session: SessionDep):
    result = session.exec(select(Client)).all()

    return templates.TemplateResponse(
        "clients.html", {"request": request, "clients": result}
    )


@ui_router.post("/clients", include_in_schema=False)
def create_client(
    request: Request,
    client_first_name: Annotated[str, Form()],
    client_last_name: Annotated[str, Form()],
    client_address: Annotated[str, Form()],
    client_city: Annotated[str, Form()],
    client_contact_number: Annotated[str, Form()],
    client_contact_email: Annotated[str, Form()],
    session=Depends(get_session),
):
    client = Client(
        first_name=client_first_name,
        last_name=client_last_name,
        address=client_address,
        city=client_city,
        phone_number=client_contact_number,
        email_address=client_contact_email,
    )
    session.add(client)
    session.commit()

    return templates.TemplateResponse(
        "clients.html", {"request": request, "clients": [client]}
    )


@ui_router.get("/venues", include_in_schema=False)
def venues(request: Request, session: SessionDep):
    result = session.exec(select(Venue)).all()

    return templates.TemplateResponse(
        "venue.html", {"request": request, "venues": result}
    )


@ui_router.post("/venues", include_in_schema=False)
def create_venue(
    request: Request,
    venue_name: Annotated[str, Form()],
    venue_address: Annotated[str, Form()],
    venue_contact_number: Annotated[str, Form()],
    venue_contact_email: Annotated[str, Form()],
    venue_capacity: int | None = Form(default=0),
    venue_notes: str = Form(default=None),
    session=Depends(get_session),
):
    if not venue_capacity:
        venue_capacity = None
    venue = Venue(
        name=venue_name,
        address=venue_address,
        contact_number=venue_contact_number,
        contact_email=venue_contact_email,
        capacity=venue_capacity,
        notes=venue_notes,
    )
    session.add(venue)
    session.commit()

    return templates.TemplateResponse(
        "venue.html", {"request": request, "venues": [venue]}
    )


@ui_router.post("/gigs", include_in_schema=False)
def create_gig(
    request: Request,
    gig_date: Annotated[date, Form()],
    gig_name: Annotated[str, Form()],
    gig_venue: Annotated[int, Form()],
    gig_client: Annotated[int, Form()],
    session=Depends(get_session),
):
    gig = Gig(
        date=gig_date,
        name=gig_name,
        time=time.fromisoformat("03:55"),
        venue_id=gig_venue,
        client_id=gig_client,
    )
    session.add(gig)
    session.commit()

    return templates.TemplateResponse(
        "gigs.html", {"request": request, "gigs": [gig]}, block_name="content"
    )


@ui_router.get("/load_venue_options", include_in_schema=False)
def get_venues_as_options(request: Request, session: SessionDep):
    venues = session.exec(select(Venue)).all()

    return templates.TemplateResponse(
        "snippets/venue_as_options.html", {"request": request, "venues": venues}
    )


@ui_router.get("/load_client_options", include_in_schema=False)
def get_clients_as_options(request: Request, session: SessionDep):
    clients = session.exec(select(Client)).all()

    return templates.TemplateResponse(
        "snippets/clients_as_options.html", {"request": request, "clients": clients}
    )


@ui_router.post("/search", include_in_schema=False)
def search(request: Request, session: SessionDep, search: Annotated[str, Form()]):
    # search_results = session.exec(select(Gig).where(Gig.name.like(f"%{search}%"))).all()
    search_results = session.exec(
        select(Gig).where(col(Gig.name).contains(search))
    ).all()
    return templates.TemplateResponse(
        "search.html", {"request": request, "search_results": search_results}
    )


@ui_router.get("/filter_gigs", include_in_schema=False)
def filter_gigs(request: Request, session: SessionDep, filter: str | None = None):
    gigs = session.exec(select(Gig)).all()
    if filter == "past":
        filtered_gigs = [gig for gig in gigs if gig.date < date.today()]
    else:
        filtered_gigs = [gig for gig in gigs if gig.date >= date.today()]
    return templates.TemplateResponse(
        "snippets/gig_results.html",
        {"request": request, "gigs": filtered_gigs},
    )
