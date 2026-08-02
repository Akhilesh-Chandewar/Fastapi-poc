import os
import tempfile

# Isolate the test database so we never touch real/dev data
TEST_DB = os.path.join(tempfile.gettempdir(), "header_auth_test.db")
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"

import pytest
from fastapi.testclient import TestClient

from main import app
from config import settings

client = TestClient(app)

API_KEY = settings.api_key
AUTH = {"X-API-Key": API_KEY}


@pytest.fixture(scope="session", autouse=True)
def _apply_lifespan():
    with TestClient(app):
        yield


@pytest.fixture()
def cleanup_users():
    yield
    from sqlmodel import Session, select
    from database import engine
    from models.user import User
    with Session(engine) as session:
        for user in session.exec(select(User)).all():
            session.delete(user)
        session.commit()


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["Status"] == "Success"


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_auth_required():
    resp = client.get("/api/v1/users")
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "http_error"


def test_auth_invalid_key():
    resp = client.get("/api/v1/users", headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401


def test_user_crud():
    payload = {"username": "alice", "email": "alice@example.com"}
    created = client.post("/api/v1/users", json=payload, headers=AUTH)
    assert created.status_code == 201
    body = created.json()
    assert body["username"] == "alice"
    assert body["is_active"] is True
    user_id = body["id"]

    listing = client.get("/api/v1/users", headers=AUTH)
    assert listing.status_code == 200
    assert any(u["id"] == user_id for u in listing.json())

    fetched = client.get(f"/api/v1/users/{user_id}", headers=AUTH)
    assert fetched.status_code == 200
    assert fetched.json()["email"] == "alice@example.com"

    updated = client.put(f"/api/v1/users/{user_id}", json={"is_active": False}, headers=AUTH)
    assert updated.status_code == 200
    assert updated.json()["is_active"] is False

    deleted = client.delete(f"/api/v1/users/{user_id}", headers=AUTH)
    assert deleted.status_code == 204
    gone = client.get(f"/api/v1/users/{user_id}", headers=AUTH)
    assert gone.status_code == 404


def test_user_duplicate(cleanup_users):
    payload = {"username": "bob", "email": "bob@example.com"}
    assert client.post("/api/v1/users", json=payload, headers=AUTH).status_code == 201
    dup = client.post("/api/v1/users", json=payload, headers=AUTH)
    assert dup.status_code == 400


def test_user_not_found():
    resp = client.get("/api/v1/users/9999", headers=AUTH)
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "http_error"


def test_book_crud(cleanup_users):
    owner = client.post(
        "/api/v1/users",
        json={"username": "carol", "email": "carol@example.com"},
        headers=AUTH,
    ).json()
    payload = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "price": 1500,
        "is_sold": False,
        "owner_id": owner["id"],
    }
    created = client.post("/api/v1/books", json=payload, headers=AUTH)
    assert created.status_code == 201
    book = created.json()
    assert book["title"] == "Clean Code"
    book_id = book["id"]

    listing = client.get("/api/v1/books", headers=AUTH)
    assert listing.status_code == 200
    assert any(b["id"] == book_id for b in listing.json())

    fetched = client.get(f"/api/v1/books/{book_id}", headers=AUTH)
    assert fetched.status_code == 200

    updated = client.put(
        f"/api/v1/books/{book_id}", json={"is_sold": True}, headers=AUTH
    )
    assert updated.status_code == 200
    assert updated.json()["is_sold"] is True

    user_books = client.get(f"/api/v1/users/{owner['id']}/books", headers=AUTH)
    assert user_books.status_code == 200
    assert any(b["id"] == book_id for b in user_books.json())

    deleted = client.delete(f"/api/v1/books/{book_id}", headers=AUTH)
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/books/{book_id}", headers=AUTH).status_code == 404


def test_book_owner_must_exist(cleanup_users):
    resp = client.post(
        "/api/v1/books",
        json={"title": "X", "author": "Y", "price": 10.0, "owner_id": 9999},
        headers=AUTH,
    )
    assert resp.status_code == 400


def test_book_filters(cleanup_users):
    user = client.post(
        "/api/v1/users",
        json={"username": "dave", "email": "dave@example.com"},
        headers=AUTH,
    ).json()
    uid = user["id"]
    client.post(
        "/api/v1/books",
        json={"title": "Python 101", "author": "Guido", "price": 9.0, "owner_id": uid},
        headers=AUTH,
    )
    client.post(
        "/api/v1/books",
        json={"title": "Rust Book", "author": "Steve", "price": 8.0, "owner_id": uid, "is_sold": True},
        headers=AUTH,
    )

    filtered = client.get("/api/v1/books", params={"title": "python"}, headers=AUTH)
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1

    sold = client.get("/api/v1/books", params={"is_sold": "true"}, headers=AUTH)
    assert all(b["is_sold"] for b in sold.json())