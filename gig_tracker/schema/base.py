import os

from sqlmodel import Session, SQLModel, create_engine

url = os.environ.get("DATABASE_URL", "sqlite+pysqlite:///:memory:")
engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
