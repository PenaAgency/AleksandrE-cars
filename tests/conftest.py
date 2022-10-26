import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, drop_database

import src.db_service as db_service
import src.models as models
from src.app import app

TEST_DATABASE_URL = (
    "postgresql+psycopg2://postgres:1234@localhost:5432/test_cars"  # noqa
)


@pytest.fixture(scope="module")
def create_test_db():
    try:
        drop_database(TEST_DATABASE_URL)
    except Exception:
        ...

    try:
        create_database(TEST_DATABASE_URL)
    except Exception:
        ...

    yield
    drop_database(TEST_DATABASE_URL)


@pytest.fixture
def testing_app(create_test_db):
    engine = create_engine(TEST_DATABASE_URL)
    models.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    def get_session():
        """Get session generator to work with the db."""
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db_service.get_session] = get_session
    client = TestClient(app)
    yield client
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_dealer_search_response(testing_app):
    """add dealer id into response body"""

    def create_item(*args):
        resp = []
        for arg in args:
            resp.append(
                testing_app.post(url="/dealer/search", json=arg).json()[0]
            )
        return resp

    return create_item


@pytest.fixture
def create_car_search_response(testing_app):
    """add car id and dealer id into response body"""

    def create_item(*args):
        resp = []
        for arg in args:
            a = testing_app.post(url="/car/search", json=arg).json()
            if a:
                resp.append(*a)

        return resp

    return create_item
