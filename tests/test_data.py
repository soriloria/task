import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_restaurant_create():
    payload = dict(
        name="NewRestaurant",
        address="NewAddress"
    )

    response = client.post("/create_restaurant/", payload)

    assert response.status_code == 201


@pytest.mark.django_db
def test_fail_restaurant_create():
    payload = dict(
        name="",
        address="Ukr123"
    )

    response = client.post("/create_restaurant/", payload)

    assert response.status_code != 201
