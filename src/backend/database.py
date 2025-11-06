from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite:///dev/data.db")
DBSession = sessionmaker(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
