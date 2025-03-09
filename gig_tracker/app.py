from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from sqlmodel import Session, select

from .logger_settings import logger
from .rate_limiter import limiter
from .routes.client_routes import client_router
from .routes.gig_routes import gig_router
from .routes.ui_routes import ui_router
from .routes.user_routes import user_router
from .routes.venue_routes import venue_router
from .schema.base import create_db_and_tables, drop_db_and_tables, get_session, seed_db
from .schema.security import Token
from .schema.user import User
from .security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_db()
    yield
    drop_db_and_tables()


app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
request: Request
app.add_exception_handler(429, _rate_limit_exceeded_handler)  # type: ignore
app.add_middleware(SlowAPIMiddleware)


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/token", response_model=Token)
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not authenticate_user(user, form_data.password):
        logger.info(f"User {form_data.username} failed to log in")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    assert user  # for mypytype checking

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


app.include_router(ui_router)
app.include_router(gig_router)
app.include_router(user_router)
app.include_router(client_router)
app.include_router(venue_router)

app.mount("/static", StaticFiles(directory="./static"), name="static")
