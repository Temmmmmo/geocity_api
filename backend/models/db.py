from __future__ import annotations

import logging
from decimal import Decimal

from sqlalchemy import DECIMAL as DbDecimal
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.settings import Settings, get_settings

from .base import BaseDbModel

settings: Settings = get_settings()
logger = logging.getLogger(__name__)


class City(BaseDbModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[Decimal] = mapped_column(DbDecimal, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(DbDecimal, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
