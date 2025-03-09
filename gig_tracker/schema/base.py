import os

import faker
from sqlmodel import Session, SQLModel, create_engine

from ..security import hash_password
from .client import Client, ClientCreate
from .gig import Gig, GigCreate
from .user import User, UserCreate
from .venue import Venue, VenueCreate

url = os.environ.get("DATABASE_URL", "sqlite+pysqlite:///:memory:")
engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


fake = faker.Faker()


def create_venues(session: Session) -> list[int]:
    venue_ids = []
    for i in range(5):
        venue = VenueCreate(
            name=fake.text(max_nb_chars=20),
            address=fake.address(),
            contact_number=fake.phone_number(),
            contact_email=fake.email(),
            capacity=fake.random_number(digits=3),
            notes=fake.paragraph(),
        )
        db_venue = Venue.model_validate(venue)

        session.add(db_venue)
        session.commit()
        session.refresh(db_venue)
        venue_ids.append(db_venue.id)

    # Create a venue that is a duplicate of one of the above
    retrieved_venue = session.get(Venue, venue_ids[0])
    assert retrieved_venue
    duplicate_venue = VenueCreate(
        name=venue.name,
        address=venue.address,
        contact_number=venue.contact_number,
        contact_email=venue.contact_email,
        capacity=venue.capacity,
        notes=venue.notes,
    )

    db_venue = Venue.model_validate(duplicate_venue)
    session.add(db_venue)
    session.commit()
    session.refresh(db_venue)
    venue_ids.append(db_venue.id)

    return venue_ids


def create_user(session: Session) -> None:
    user = UserCreate(
        username="user1",
        first_name="Dave",
        last_name="Westerveld",
        email_address="fake@fake.com",
        password="password",
    )
    pwd_data = {"hashed_password": hash_password(user.password)}
    db_user = User.model_validate(user, update=pwd_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)


def create_clients(session: Session) -> list[int]:
    client_ids = []
    for _ in range(5):
        client = ClientCreate(
            email_address=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            city=fake.city(),
            province=fake.state(),
            zip=fake.postalcode(),
            country=fake.country(),
        )

        db_client = Client.model_validate(client)
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        client_ids.append(db_client.id)
    return client_ids


def create_gigs(session: Session, venue_ids: list[int], client_ids: list[int]) -> None:
    for _ in range(5):
        gig = GigCreate(
            venue_id=fake.random_element(venue_ids),
            client_id=fake.random_element(client_ids),
            date=fake.date(),
            time=fake.time(pattern="%H:%M"),
            name=fake.text(max_nb_chars=20),
        )
        db_gig = Gig.model_validate(gig)

        session.add(db_gig)
        session.commit()
        session.refresh(db_gig)


def seed_db():
    with Session(engine) as session:
        venue_ids = create_venues(session)
        create_user(session)
        client_ids = create_clients(session)
        create_gigs(session, venue_ids, client_ids)
