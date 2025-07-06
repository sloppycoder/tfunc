import pytest

from settings import settings
from tests.jwt_utils import create_jwt_token


async def test_info(client):
    response = client.get("/api/info")
    assert response.status_code == 200


async def test_secret_unauthenticated(client):
    response = client.get("/api/secret")
    assert response.status_code == 403


async def test_secret_authenticated(client):
    jwt_token = create_jwt_token(scope="read:data", audience=settings.api_audience)
    response = client.get("/api/secret", headers={"Authorization": "Bearer " + jwt_token})
    assert response.status_code == 200



async def test_get_something_useful(client):
    response = client.get("/api/useful")
    # feature flag defaults to true.
    # flags.json will return false, if it works properly
    # the test will be successful only if flagd is return the correct data.
    assert response.status_code == 403





async def test_get_user(client, test_db):
    response = client.get("/api/users/root")
    assert response.status_code == 200



@pytest.mark.skipif(settings.async_orm is False, reason="Async ORM is disabled")
async def test_get_user_aysnc(client, test_db):
    response = client.get("/api/async/users/root")
    assert response.status_code == 200




