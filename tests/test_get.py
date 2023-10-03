import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_restaurants_show():
    response = client.get('/show_restaurants/')

    assert response.status_code == 200
