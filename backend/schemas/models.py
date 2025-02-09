from decimal import Decimal
from typing import Optional

from fastapi.params import Query
from pydantic import field_validator, model_validator, root_validator

from backend.exceptions import InvalidParameters, MissingParameters
from backend.schemas.base import Base


class OuterAPIPosition(Base):
    outer_api_name: str | None = None
    longitude: Decimal  # Долгота
    latitude: Decimal  # Широта


class CityGet(Base):
    id: int
    name: str
    outer_api_name: str | None = None
    longitude: Decimal
    latitude: Decimal
    distance: Decimal | None = None


class CityPost(Base):
    id: int
    name: str
    outer_api_name: str | None = None
    longitude: Decimal
    latitude: Decimal
