from decimal import Decimal

from backend.schemas.base import Base


class Coordinates(Base):
    longitude: Decimal  # Долгота
    latitude: Decimal  # Широта


class CityGet(Base):
    id: int
    name: str
    longitude: Decimal
    latitude: Decimal
    distance: Decimal | None = None
