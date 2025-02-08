import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.models.db import *
from backend.routes import app
from backend.schemas.models import Coordinates
from backend.settings import Settings


@pytest.fixture
def client(mocker):
    user_mock = mocker.patch(
        "backend.utils.yandex_geocoder.YandexGeocoderAPI.get_coordinates"
    )
    user_mock.return_value = Coordinates(longitude=50, latitude=40)
    client = TestClient(app)
    return client


@pytest.fixture
def dbsession() -> Session:
    settings = Settings()
    engine = create_engine(str(settings.DB_DSN), pool_pre_ping=True)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session


@pytest.fixture
def cities(dbsession):
    """
    Creates several cities with different IDs and attributes.
    """
    cities_data = [
        (1, "City1", 37.62, 55.75),
        (2, "City2", 37.72, 55.85),
        (3, "City3", 37.82, 55.95),
        (4, "City4", 37.92, 56.05),
    ]

    cities = [
        City(
            id=city_id,
            name=name,
            longitude=longitude,
            latitude=latitude,
        )
        for city_id, name, longitude, latitude in cities_data
    ]

    for city in cities:
        dbsession.add(city)
    dbsession.commit()
    yield cities
    for city in cities:
        dbsession.refresh(city)
        dbsession.delete(city)
    dbsession.commit()
