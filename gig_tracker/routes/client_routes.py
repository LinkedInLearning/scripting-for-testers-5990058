import random
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..schema.base import get_session
from ..schema.client import Client, ClientCreate, ClientPublic
from ..security import verify_token

SessionDep = Annotated[Session, Depends(get_session)]
client_router = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class IntermitentErrorGenerator:
    def __init__(self):
        self.counter = 0
        self.created_client = False

    def _increment_count(self):
        self.counter += 1

    def mark_client_created(self):
        self.created_client = True

    def should_return_intermittent_error(self):
        self._increment_count()

        if self.counter > 2 and self.created_client:
            self.created_client = False
            if random.random() < 0.2:
                self.counter = 0
                return True
            return False
        return False


error_generator = IntermitentErrorGenerator()


@client_router.get("/clients", response_model=list[ClientPublic])
def get_clients(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    clients = session.exec(select(Client)).all()
    return clients


@client_router.get("/clients/{client_id}", response_model=ClientPublic)
def get_client(
    client_id: int,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    if error_generator.should_return_intermittent_error():
        raise HTTPException(status_code=500, detail="Intermittent error")
    client = session.get(Client, client_id)
    return client


@client_router.post(
    "/clients",
    response_model=ClientPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    client: ClientCreate,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    error_generator.mark_client_created()
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    phone_number = {"phone_number": f"+{client.phone_number}"}
    db_client = Client.model_validate(client, update=phone_number)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client
