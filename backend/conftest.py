import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from auth import get_db
from database import Base
from main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def _register_and_login(client, name, email):
    client.post("/signup", json={"name": name, "email": email, "password": "password123"})
    res = client.post("/login", json={"email": email, "password": "password123"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture()
def auth_headers(client):
    return _register_and_login(client, "Test User", "test@example.com")


@pytest.fixture()
def other_headers(client):
    return _register_and_login(client, "Other User", "other@example.com")