import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def unique_user():
    identifier = uuid.uuid4().hex[:8]
    return {
        "username": f"testuser_{identifier}",
        "email": f"test_{identifier}@example.com",
        "password": "StrongPass123",
        "phone": "9876543210",
        "monthly_income": 50000,
    }


def create_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_user_success():
    payload = unique_user()
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert data["role"] == "user"


def test_register_duplicate_username():
    payload = unique_user()
    first = client.post("/auth/register", json=payload)
    assert first.status_code == 201

    duplicate = payload.copy()
    duplicate["email"] = f"new_{uuid.uuid4().hex[:6]}@example.com"
    resp = client.post("/auth/register", json=duplicate)
    assert resp.status_code == 409
    assert resp.json()["error"] == "DuplicateUserError"


def test_register_invalid_email_format():
    payload = unique_user()
    payload["email"] = "invalid-email"
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 422
    assert "value is not a valid email address" in str(resp.json()["detail"]) or "Not an email" in str(resp.json()["detail"])


def test_login_correct_credentials():
    payload = unique_user()
    client.post("/auth/register", json=payload)

    resp = client.post("/auth/login", json={"username": payload["username"], "password": payload["password"]})
    assert resp.status_code == 200
    body = resp.json()
    assert body["message"] == "Login successful"
    assert "access_token" in body


def test_login_wrong_password():
    payload = unique_user()
    client.post("/auth/register", json=payload)

    resp = client.post("/auth/login", json={"username": payload["username"], "password": "WrongPass123"})
    assert resp.status_code == 401
    body = resp.json()
    assert body["error"] == "InvalidCredentialsError"
