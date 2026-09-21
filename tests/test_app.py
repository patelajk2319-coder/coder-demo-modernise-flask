import json

import pytest

import app as app_module
from app import app

client = app.test_client()


@pytest.fixture(autouse=True)
def restore_data_file():
    original = app_module.DATA_FILE.read_text()
    original_items = json.loads(original)
    yield
    app_module.DATA_FILE.write_text(original)
    app_module.ITEMS[:] = original_items


def test_get_items():
    response = client.get("/items")

    assert response.status_code == 200
    body = response.get_json()
    assert isinstance(body, list)
    assert len(body) == 3
    assert body[0] == {"id": 1, "name": "Bracket", "quantity": 17}


def test_get_item():
    response = client.get("/items/2")

    assert response.status_code == 200
    assert response.get_json() == {"id": 2, "name": "Flange", "quantity": 8}


def test_get_item_not_found():
    response = client.get("/items/999")

    assert response.status_code == 404


def test_create_item():
    response = client.post("/items", json={"name": "Washer", "quantity": 100})

    assert response.status_code == 201
    body = response.get_json()
    assert body == {"id": 4, "name": "Washer", "quantity": 100}

    persisted = json.loads(app_module.DATA_FILE.read_text())
    assert persisted[-1] == body


def test_create_item_missing_fields():
    response = client.post("/items", json={"name": "Washer"})

    assert response.status_code == 400
