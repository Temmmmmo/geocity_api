import asyncio

from backend.routes.models.models import Coordinates
from aiohttp import ClientSession
from backend.settings import Settings


class YandexGeocoderSettings(Settings):
    YANDEX_GEOCODER_BASE_URL: str = "https://geocode-maps.yandex.ru/1.x"
    YANDEX_GEOCODER_LANGUAGE: str = (
        "ru_RU"  # Возможные значения https://yandex.ru/dev/geocode/doc/ru/request
    )
    YANDEX_GEOCODER_API_KEY: str = "6465a350-1068-4493-adc9-f3fd3c231481"


class YandexGeocoderAPI:
    settings = YandexGeocoderSettings()

    @classmethod
    async def get_coordinates(cls, city_name: str) -> Coordinates:
        query: dict = {
            "apikey": cls.settings.YANDEX_GEOCODER_API_KEY,
            "geocode": city_name,
            "format": "json",
        }
        print(query.get("apikey"))
        async with ClientSession() as session:
            print(query)
            async with session.get(
                cls.settings.YANDEX_GEOCODER_BASE_URL, params=query
            ) as response:
                json_response = await response.json()
                all_positions: list = (
                    json_response.get("response", {})
                    .get("GeoObjectCollection", {})
                    .get("featureMember", {})
                )
                most_relevant_position = all_positions[0]
                result_position = (
                    most_relevant_position.get("GeoObject", {})
                    .get("Point", {})
                    .get("pos", "")
                    .split()
                )
                if result_position:
                    return Coordinates(
                        longitude=result_position[0], latitude=result_position[1]
                    )
