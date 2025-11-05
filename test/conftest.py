import pytest
from data_sample import init_sample_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base


@pytest.fixture(scope="session", autouse=True)
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    init_sample_data(session)
    return session
