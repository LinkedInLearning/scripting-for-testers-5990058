from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email_address: EmailStr
    first_name: str
    last_name: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
