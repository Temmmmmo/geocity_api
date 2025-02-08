import datetime
import logging
from decimal import Decimal
from typing import Literal, Optional
from uuid import UUID

import aiohttp
from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query as DbQuery

from backend.exceptions import AlreadyExists, MissingParameters, ObjectNotFound
from backend.models import City
from backend.schemas.base import StatusResponseModel
from backend.schemas.models import CityGet, Coordinates
from backend.settings import Settings, get_settings
from backend.utils.yandex_geocoder import YandexGeocoderAPI

settings: Settings = get_settings()
city = APIRouter(prefix="/city", tags=["City"])
logger = logging.getLogger(__name__)


@city.post("", response_model=CityGet)
async def create_city(city_name: str) -> CityGet:
    """
    Создает город с его координатами, взятыми из YandexGeocoderAPI, в базе данных

    Обязательный параметр: **city_name - название города**
    """
    coordinates: Coordinates = await YandexGeocoderAPI.get_coordinates(city_name)
    if coordinates is None:
        raise ObjectNotFound(Coordinates, city_name)
    check_city: DbQuery = City.query(session=db.session).filter(City.name == city_name)
    if check_city.one_or_none() is not None:
        raise AlreadyExists(City, city_name)
    check_city: DbQuery = City.query(session=db.session).filter(
        and_(
            City.longitude == coordinates.longitude,
            City.latitude == coordinates.latitude,
        )
    )
    if check_city.one_or_none() is not None:
        raise AlreadyExists(
            City, f"latitude, longitude = {coordinates.latitude, coordinates.longitude}"
        )
    new_city = City.create(
        session=db.session,
        name=city_name,
        longitude=coordinates.longitude,
        latitude=coordinates.latitude,
    )
    return CityGet.model_validate(new_city)


@city.get("", response_model=list[CityGet])
async def get_cities(
    longitude: Optional[Decimal] = None, latitude: Optional[Decimal] = None
) -> list[CityGet]:
    """
    Возвращает все города, имеющиеся в базе.
    Если одновременно переданы query-параметры *longitude(Долгота)*, *latitude(Широта)*,
    то вернется два ближайших к этим координатам города.
    """
    if longitude is None and latitude is not None:
        raise MissingParameters("longitude")
    if latitude is None and longitude is not None:
        raise MissingParameters("latitude")
    result: list[CityGet] = []
    if longitude is None and latitude is None:
        cities: list[City] = City.query(session=db.session).all()
        for city in cities:
            result.append(CityGet.model_validate(city))
        return result
    sorted_cities: list[City] = sorted(
        City.query(session=db.session).all(),
        key=lambda item: item.distance_to(longitude, latitude),
    )
    for city in sorted_cities:
        result.append(
            CityGet(
                id=city.id,
                name=city.name,
                longitude=city.longitude,
                latitude=city.latitude,
                distance=city.distance_to(longitude, latitude),
            )
        )
        if len(result) == settings.NEAREST_CITY_COUNT:
            break
    return result


@city.get("/{city_id}", response_model=CityGet)
async def get_city(
    city_id: int,
    longitude: Optional[Decimal] = None,
    latitude: Optional[Decimal] = None,
) -> CityGet:
    """
    Возвращает город по его идентификатору в базе данных.
    Если одновременно переданы параметры longitude, latitude, то также вернет расстояние от данной точки до данного города
    """
    if longitude is None and latitude is not None:
        raise MissingParameters("longitude")
    if latitude is None and longitude is not None:
        raise MissingParameters("latitude")
    city: City = City.get(session=db.session, id=city_id)
    if latitude is not None and longitude is not None:
        return CityGet(
            id=city.id,
            name=city.name,
            longitude=city.longitude,
            latitude=city.latitude,
            distance=city.distance_to(longitude, latitude),
        )
    return CityGet.model_validate(city)


@city.delete("/{city_id}", response_model=StatusResponseModel)
async def delete_cities(city_id: int) -> StatusResponseModel:
    """
    Удаляет город из базы данных по его id
    """
    City.delete(session=db.session, id=city_id)
    return StatusResponseModel(
        status="Success",
        message=f"City with id {city_id} has been deleted from database",
        ru=f"Город с идентификатором {city_id} был удален из базы данных",
    )
