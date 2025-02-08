import pytest
from starlette import status

from backend.models.db import *

logger = logging.getLogger(__name__)
url: str = "/city"


@pytest.mark.parametrize(
    "response_status, city_name",
    [(status.HTTP_200_OK, "City10"), (status.HTTP_409_CONFLICT, "City1")],
)
def test_create_city(client, dbsession, response_status, city_name, cities):
    query = {"city_name": city_name}
    post_response = client.post(url, params=query)
    assert post_response.status_code == response_status
    if response_status == status.HTTP_200_OK:
        assert post_response.json()["name"] == query["city_name"]
        delete_response = client.delete(f'{url}/{post_response.json()["id"]}')
        assert delete_response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "city_id,response_status",
    [
        (1, status.HTTP_200_OK),
        (2, status.HTTP_200_OK),
        (0, status.HTTP_404_NOT_FOUND),
    ],
)
def test_get_city(client, city_id, response_status, cities):
    get_response = client.get(f"{url}/{city_id}")
    assert get_response.status_code == response_status
    if response_status == status.HTTP_200_OK:
        json_response = get_response.json()
        assert "id" in json_response
        assert "name" in json_response


@pytest.mark.parametrize(
    "city_id,expected_status",
    [(0, status.HTTP_404_NOT_FOUND)],
)
def test_delete_city(client, city_id, expected_status):
    delete_response = client.delete(f"{url}/{city_id}")
    assert delete_response.status_code == expected_status
    if expected_status == status.HTTP_200_OK:
        get_response = client.get(f"{url}/{city_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "params,response_status",
    [
        ({"longitude": 37.62, "latitude": 55.75}, status.HTTP_200_OK),
        (None, status.HTTP_200_OK),
    ],
)
def test_get_cities_by_coordinates(client, cities, params, response_status):
    get_response = client.get(url, params=params)
    assert get_response.status_code == response_status
    if response_status == status.HTTP_200_OK:
        json_response = get_response.json()
