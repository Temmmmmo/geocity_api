import asyncio
import logging
from decimal import Decimal

from aiohttp import ClientSession

from backend.schemas.models import OuterAPIPosition
from backend.settings import Settings

logger = logging.getLogger(__name__)


class YandexGeocoderSettings(Settings):
    YANDEX_GEOCODER_BASE_URL: str = "https://geocode-maps.yandex.ru/1.x"
    YANDEX_GEOCODER_LANGUAGE: str = (
        "ru_RU"  # Возможные значения https://yandex.ru/dev/geocode/doc/ru/request
    )
    YANDEX_GEOCODER_API_KEY: str | None = "6465a350-1068-4493-adc9-f3fd3c231481"


class YandexGeocoderAPI:
    settings = YandexGeocoderSettings()

    @classmethod
    async def get_coordinates(cls, city_name: str) -> OuterAPIPosition | None:
        """Возвращает координаты города по его названию. Если город с таким названием не найден, то возвращает None."""
        query: dict = {
            "apikey": cls.settings.YANDEX_GEOCODER_API_KEY,
            "geocode": city_name,
            "format": "json",
            "kind": "locality",
        }
        async with ClientSession() as session:

            async with session.get(
                cls.settings.YANDEX_GEOCODER_BASE_URL, params=query
            ) as response:
                json_response = await response.json()
                all_positions: list = (
                    json_response.get("response", {})
                    .get("GeoObjectCollection", {})
                    .get("featureMember", [])
                )
                if not all_positions:
                    return None
                most_relevant_position: dict = {}
                for position in all_positions:
                    pos_data = (
                        position.get("GeoObject", {})
                        .get("metaDataProperty", {})
                        .get("GeocoderMetaData", {})
                    )
                    if pos_data.get("kind") is not None and pos_data.get("kind") in [
                        "locality",
                        "province",
                    ]:
                        most_relevant_position = position
                        break
                result_position = (
                    most_relevant_position.get("GeoObject", {})
                    .get("Point", {})
                    .get("pos", "")
                    .split()
                )
                if result_position:
                    return OuterAPIPosition(
                        outer_api_name=most_relevant_position.get("GeoObject", {}).get(
                            "name"
                        ),
                        longitude=Decimal(result_position[0]),
                        latitude=Decimal(result_position[1]),
                    )
                return None
