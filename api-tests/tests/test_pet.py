import pytest
from jsonschema import validate
from utils.config import ENDPOINTS
from utils.data_builder import build_pet_payload
from data.schemas import PET_SCHEMA


@pytest.mark.pet
@pytest.mark.smoke
class TestPetCreation:

    def test_create_pet_with_valid_data_returns_200(self, api_client, pet_payload):
        response = api_client.post(ENDPOINTS["pet"], json=pet_payload)

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=PET_SCHEMA)
        assert body["id"] == pet_payload["id"]
        assert body["name"] == pet_payload["name"]
        assert body["status"] == pet_payload["status"]

        api_client.delete(f"{ENDPOINTS['pet']}/{pet_payload['id']}")

    def test_create_pet_with_minimal_payload(self, api_client):
        minimal = {"name": "Buddy", "photoUrls": ["http://example.com/photo.jpg"]}
        response = api_client.post(ENDPOINTS["pet"], json=minimal)

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "Buddy"
        assert "id" in body

        api_client.delete(f"{ENDPOINTS['pet']}/{body['id']}")


@pytest.mark.pet
class TestPetRetrieval:

    def test_get_existing_pet_returns_correct_data(self, api_client, new_pet):
        response = api_client.get(f"{ENDPOINTS['pet']}/{new_pet['id']}")

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=PET_SCHEMA)
        assert body["id"] == new_pet["id"]
        assert body["name"] == new_pet["name"]

    def test_get_nonexistent_pet_returns_404(self, api_client):
        response = api_client.get(f"{ENDPOINTS['pet']}/0")
        assert response.status_code == 404

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, api_client, status):
        response = api_client.get(ENDPOINTS["pet_find_by_status"], params={"status": status})

        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        if pets:
            assert all(p.get("status") == status for p in pets[:10])


@pytest.mark.pet
class TestPetUpdate:

    def test_update_existing_pet(self, api_client, new_pet):
        new_pet["name"] = "UpdatedName"
        new_pet["status"] = "sold"

        response = api_client.put(ENDPOINTS["pet"], json=new_pet)

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "UpdatedName"
        assert body["status"] == "sold"


@pytest.mark.pet
class TestPetDeletion:

    def test_delete_existing_pet(self, api_client, pet_payload):
        api_client.post(ENDPOINTS["pet"], json=pet_payload)

        response = api_client.delete(f"{ENDPOINTS['pet']}/{pet_payload['id']}")
        assert response.status_code == 200

        get_response = api_client.get(f"{ENDPOINTS['pet']}/{pet_payload['id']}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_pet_returns_404(self, api_client):
        response = api_client.delete(f"{ENDPOINTS['pet']}/0")
        assert response.status_code == 404
