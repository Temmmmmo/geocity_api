import math
from decimal import Decimal


def calculate_distance(
    lat1: Decimal, lon1: Decimal, lat2: Decimal, lon2: Decimal
) -> Decimal:
    """
    Возвращает расстояние между двумя точками на сфере используя формулу гаверсина.
    """
    R = 6371  # Радиус Земли в километрах
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c

    return Decimal(distance)
