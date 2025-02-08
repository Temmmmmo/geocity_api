from __future__ import annotations

import logging
from decimal import Decimal

from sqlalchemy import DECIMAL as DbDecimal
from sqlalchemy import (Boolean, Integer, String, UnaryExpression,
                        UniqueConstraint, func, nulls_last)
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from backend.settings import Settings, get_settings
from backend.utils.distance_calculator import calculate_distance

from .base import BaseDbModel

settings: Settings = get_settings()
logger = logging.getLogger(__name__)


class City(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[Decimal] = mapped_column(DbDecimal, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(DbDecimal, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @hybrid_method
    def distance_to(self, longitude: Decimal, latitude: Decimal) -> Decimal:
        return calculate_distance(latitude, longitude, self.latitude, self.longitude)
