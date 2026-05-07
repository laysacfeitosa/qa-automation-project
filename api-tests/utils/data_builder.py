import random
from datetime import datetime, timezone
from faker import Faker

fake = Faker()


def build_pet_payload(pet_id: int | None = None, status: str = "available") -> dict:
    return {
        "id": pet_id or random.randint(10**8, 10**9),
        "category": {"id": random.randint(1, 100), "name": fake.word()},
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [{"id": random.randint(1, 100), "name": fake.word()}],
        "status": status,
    }


def build_user_payload(user_id: int | None = None) -> dict:
    username = f"{fake.user_name()}_{random.randint(1000, 9999)}"
    return {
        "id": user_id or random.randint(10**8, 10**9),
        "username": username,
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
        "phone": fake.phone_number(),
        "userStatus": 1,
    }


def build_order_payload(order_id: int | None = None, pet_id: int | None = None) -> dict:
    return {
        "id": order_id or random.randint(1, 10),
        "petId": pet_id or random.randint(10**8, 10**9),
        "quantity": random.randint(1, 5),
        "shipDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "status": "placed",
        "complete": True,
    }
