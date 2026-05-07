import os

BASE_URL = os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2")

ENDPOINTS = {
    "pet": f"{BASE_URL}/pet",
    "pet_find_by_status": f"{BASE_URL}/pet/findByStatus",
    "store_order": f"{BASE_URL}/store/order",
    "store_inventory": f"{BASE_URL}/store/inventory",
    "user": f"{BASE_URL}/user",
    "user_login": f"{BASE_URL}/user/login",
    "user_logout": f"{BASE_URL}/user/logout",
    "user_create_with_list": f"{BASE_URL}/user/createWithList",
}

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

REQUEST_TIMEOUT = 30
