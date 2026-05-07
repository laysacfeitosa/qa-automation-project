import os

BASE_URL = os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com/")

USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked": {"username": "locked_out_user", "password": "secret_sauce"},
    "problem": {"username": "problem_user", "password": "secret_sauce"},
    "performance": {"username": "performance_glitch_user", "password": "secret_sauce"},
}

CHECKOUT_INFO = {
    "first_name": "João",
    "last_name": "Silva",
    "postal_code": "60000-000",
}

DEFAULT_TIMEOUT = 10
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
