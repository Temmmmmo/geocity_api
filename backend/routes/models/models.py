from backend.routes.models.base import Base


class Coordinates(Base):
    longitude: str  # Долгота
    latitude: str  # Широта
