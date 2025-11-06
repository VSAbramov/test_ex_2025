import pytest
from data_sample import init_sample_data
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from backend import database
from backend.database import get_db_session
from backend.main import app
from backend.models import Base

client = TestClient(app)


@pytest.fixture(scope="session")
def Session():
    # init in memmory db connection
    engine = create_engine(
        "sqlite:///:memory:?cache=shared&uri=true",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker(bind=engine)
    # DBSession = scoped_session(sessionmaker(bind=engine))

    # monkey patch connection on client side
    database.engine = engine
    database.DBSession = sessionmaker(bind=engine)

    # initialize data
    session = DBSession()
    init_sample_data(session)
    session.close()

    return DBSession


@pytest.fixture
def db(Session):
    db_session = Session()

    def override_get_db():
        return db_session

    # mocker.patch("backend.api.get_db_session", return_value=db_session)
    app.dependency_overrides[get_db_session] = override_get_db
    try:
        return db_session
    finally:
        db_session.close()
