from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["Status"] == "Success"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_menu():
    response = client.get("/menu")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["count"] == 5
    assert len(body["menu_items"]) == 5


def test_get_menu_by_category():
    response = client.get("/menu", params={"category": "Pizza"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["menu_items"][0]["name"] == "Margherita Pizza"


def test_get_menu_by_category_case_insensitive():
    response = client.get("/menu", params={"category": "pizza"})
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_get_menu_by_availability():
    response = client.get("/menu", params={"available": "true"})
    assert response.status_code == 200
    assert all(item["is_available"] for item in response.json()["menu_items"])


def test_get_menu_item_found():
    response = client.get("/menu/1")
    assert response.status_code == 200
    assert response.json()["menu_items"][0]["name"] == "Margherita Pizza"


def test_get_menu_item_not_found():
    response = client.get("/menu/999")
    assert response.status_code == 404
    body = response.json()
    assert body["status"] == "error"
    assert body["error_code"] == "item_not_found"


def test_get_menu_item_invalid_id():
    response = client.get("/menu/0")
    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_request"


def test_get_menu_item_non_numeric():
    response = client.get("/menu/abc")
    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"


def test_get_menu_invalid_category():
    response = client.get("/menu", params={"category": "Sushi"})
    assert response.status_code == 400
    assert response.json()["error_code"] == "invalid_category"


def test_get_menu_category_too_long():
    response = client.get("/menu", params={"category": "x" * 51})
    assert response.status_code == 422
    body = response.json()
    assert body["error_code"] == "validation_error"
    assert body["details"] is not None
    assert body["details"][0]["loc"] == ["query", "category"]


def test_error_response_shape():
    response = client.get("/menu/999")
    body = response.json()
    assert set(body) == {"status", "error_code", "message", "details"}
    assert body["details"] is None
