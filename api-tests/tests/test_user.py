import pytest
from jsonschema import validate
from utils.config import ENDPOINTS
from utils.data_builder import build_user_payload
from data.schemas import USER_SCHEMA


@pytest.mark.user
@pytest.mark.smoke
class TestUserCreation:

    def test_create_single_user(self, api_client, user_payload):
        response = api_client.post(ENDPOINTS["user"], json=user_payload)

        assert response.status_code == 200
        body = response.json()
        assert body["code"] == 200
        assert str(user_payload["id"]) in body["message"]

        api_client.delete(f"{ENDPOINTS['user']}/{user_payload['username']}")

    def test_create_users_with_list(self, api_client):
        users = [build_user_payload() for _ in range(3)]
        response = api_client.post(ENDPOINTS["user_create_with_list"], json=users)

        assert response.status_code == 200

        for u in users:
            api_client.delete(f"{ENDPOINTS['user']}/{u['username']}")


@pytest.mark.user
class TestUserRetrieval:

    def test_get_existing_user_by_username(self, api_client, new_user):
        response = api_client.get(f"{ENDPOINTS['user']}/{new_user['username']}")

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=USER_SCHEMA)
        assert body["username"] == new_user["username"]
        assert body["email"] == new_user["email"]

    def test_get_nonexistent_user_returns_404(self, api_client):
        response = api_client.get(f"{ENDPOINTS['user']}/usuario_que_nao_existe_xyz_123")
        assert response.status_code == 404


@pytest.mark.user
class TestUserUpdate:

    def test_update_existing_user(self, api_client, new_user):
        new_user["firstName"] = "NomeAtualizado"
        new_user["email"] = "atualizado@teste.com"

        response = api_client.put(
            f"{ENDPOINTS['user']}/{new_user['username']}", json=new_user
        )
        assert response.status_code == 200

        get_response = api_client.get(f"{ENDPOINTS['user']}/{new_user['username']}")
        assert get_response.status_code == 200
        body = get_response.json()
        assert body["firstName"] == "NomeAtualizado"
        assert body["email"] == "atualizado@teste.com"


@pytest.mark.user
class TestUserAuthentication:

    def test_login_with_valid_credentials(self, api_client, new_user):
        response = api_client.get(
            ENDPOINTS["user_login"],
            params={"username": new_user["username"], "password": new_user["password"]},
        )
        assert response.status_code == 200
        body = response.json()
        assert "logged in user session" in body["message"].lower()

    def test_logout(self, api_client):
        response = api_client.get(ENDPOINTS["user_logout"])
        assert response.status_code == 200


@pytest.mark.user
class TestUserDeletion:

    def test_delete_existing_user(self, api_client, user_payload):
        api_client.post(ENDPOINTS["user"], json=user_payload)

        response = api_client.delete(f"{ENDPOINTS['user']}/{user_payload['username']}")
        assert response.status_code == 200

    def test_delete_nonexistent_user_returns_404(self, api_client):
        response = api_client.delete(f"{ENDPOINTS['user']}/inexistente_xyz_123_abc")
        assert response.status_code == 404
