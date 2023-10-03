import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register():
    payload = dict(
        name="Igor",
        password="Qwer1234"
    )

    response = client.post("/register/", payload)

    data = response.data

    assert data['name'] == payload['name']
    assert "password" not in data


@pytest.mark.django_db
def test_login():
    payload = dict(
        name="Igor",
        password="Qwer1234"
    )

    client.post("/register/", payload)

    response = client.post('/login/', dict(name="Igor", password="Qwer1234"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_fail():
    response = client.post('/login/', dict(name="NotIgor", password="Qwer1234"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_logout():
    response = client.get('/logout/')

    assert response.data == {"Logged out"}
