import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@pytest.fixture(scope="function")
def create_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def update_pet(create_pet):
    pet_id = create_pet["id"]
    payload = {
        "id": pet_id,
        "name": "Buddy Updated",
        "status": "sold"
    }
    response = requests.put(f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def delete_pet(create_pet):
    pet_id = create_pet["id"]
    response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

    assert response.status_code == 200
