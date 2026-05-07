import pytest
from jsonschema import validate
from utils.config import ENDPOINTS
from data.schemas import ORDER_SCHEMA


@pytest.mark.store
@pytest.mark.smoke
class TestStoreInventory:

    def test_get_inventory_returns_dict(self, api_client):
        response = api_client.get(ENDPOINTS["store_inventory"])

        assert response.status_code == 200
        inventory = response.json()
        assert isinstance(inventory, dict)
        assert all(isinstance(v, int) for v in inventory.values())


@pytest.mark.store
class TestStoreOrderCreation:

    def test_create_order_with_valid_data(self, api_client, order_payload):
        response = api_client.post(ENDPOINTS["store_order"], json=order_payload)

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=ORDER_SCHEMA)
        assert body["id"] == order_payload["id"]
        assert body["petId"] == order_payload["petId"]

        api_client.delete(f"{ENDPOINTS['store_order']}/{order_payload['id']}")


@pytest.mark.store
class TestStoreOrderRetrieval:

    def test_get_existing_order(self, api_client, new_order):
        response = api_client.get(f"{ENDPOINTS['store_order']}/{new_order['id']}")

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=ORDER_SCHEMA)
        assert body["id"] == new_order["id"]

    @pytest.mark.parametrize("invalid_id", [-1, 9999])
    def test_get_invalid_order_returns_404(self, api_client, invalid_id):
        response = api_client.get(f"{ENDPOINTS['store_order']}/{invalid_id}")
        assert response.status_code == 404


@pytest.mark.store
class TestStoreOrderDeletion:

    def test_delete_existing_order(self, api_client, order_payload):
        api_client.post(ENDPOINTS["store_order"], json=order_payload)

        response = api_client.delete(f"{ENDPOINTS['store_order']}/{order_payload['id']}")
        assert response.status_code == 200

        get_response = api_client.get(f"{ENDPOINTS['store_order']}/{order_payload['id']}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_order_returns_404(self, api_client):
        response = api_client.delete(f"{ENDPOINTS['store_order']}/0")
        assert response.status_code == 404
