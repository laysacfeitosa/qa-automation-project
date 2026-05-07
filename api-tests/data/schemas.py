PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "photoUrls"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "photoUrls": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string", "enum": ["available", "pending", "sold"]},
        "category": {"type": "object"},
        "tags": {"type": "array"},
    },
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "username"],
    "properties": {
        "id": {"type": "integer"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "phone": {"type": "string"},
        "userStatus": {"type": "integer"},
    },
}

ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "shipDate": {"type": "string"},
        "status": {"type": "string", "enum": ["placed", "approved", "delivered"]},
        "complete": {"type": "boolean"},
    },
}

API_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["code", "message"],
    "properties": {
        "code": {"type": "integer"},
        "type": {"type": "string"},
        "message": {"type": "string"},
    },
}
