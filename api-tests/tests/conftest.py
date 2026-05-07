import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from utils.api_client import ApiClient
from utils.data_builder import build_pet_payload, build_user_payload, build_order_payload
from utils.config import ENDPOINTS


@pytest.fixture(scope="session")
def api_client():
    client = ApiClient()
    yield client
    client.close()


@pytest.fixture
def new_pet(api_client):
    """Cria um pet e garante limpeza ao final."""
    payload = build_pet_payload()
    response = api_client.post(ENDPOINTS["pet"], json=payload)
    assert response.status_code == 200, f"Falha ao criar pet: {response.text}"
    yield payload
    api_client.delete(f"{ENDPOINTS['pet']}/{payload['id']}")


@pytest.fixture
def new_user(api_client):
    """Cria um usuário e garante limpeza ao final."""
    payload = build_user_payload()
    response = api_client.post(ENDPOINTS["user"], json=payload)
    assert response.status_code == 200, f"Falha ao criar usuário: {response.text}"
    yield payload
    api_client.delete(f"{ENDPOINTS['user']}/{payload['username']}")


@pytest.fixture
def new_order(api_client):
    """Cria um pedido e garante limpeza ao final."""
    payload = build_order_payload()
    response = api_client.post(ENDPOINTS["store_order"], json=payload)
    assert response.status_code == 200, f"Falha ao criar pedido: {response.text}"
    yield payload
    api_client.delete(f"{ENDPOINTS['store_order']}/{payload['id']}")


@pytest.fixture
def pet_payload():
    return build_pet_payload()


@pytest.fixture
def user_payload():
    return build_user_payload()


@pytest.fixture
def order_payload():
    return build_order_payload()
