from decimal import Decimal

from backend.routes.models.base import Base


class Coordinates(Base):
    longitude: Decimal  # Долгота
    latitude: Decimal  # Широта
