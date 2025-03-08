from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select

from ..schema.base import get_session
from ..schema.user import User, UserCreate, UserPublic
from ..security import authenticate_user, hash_password

SessionDep = Annotated[Session, Depends(get_session)]

user_router = APIRouter(prefix="/api")

basic_auth_security = HTTPBasic()


@user_router.get("/users/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    session: SessionDep,
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth_security)],
):
    username = credentials.username
    password = credentials.password
    user = session.exec(select(User).where(User.username == username)).first()
    if not authenticate_user(user, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = session.get(User, user_id)
    return user


@user_router.get("/users", response_model=UserPublic)
def get_users(
    session: SessionDep,
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_auth_security)],
):
    username = credentials.username
    password = credentials.password
    user = session.exec(select(User).where(User.username == username)).first()
    if not authenticate_user(user, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user


@user_router.post(
    "/users",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate, session: SessionDep):
    pwd_data = {"hashed_password": hash_password(user.password)}
    db_user = User.model_validate(user, update=pwd_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
