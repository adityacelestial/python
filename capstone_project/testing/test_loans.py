import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def unique_user():
    identifier = uuid.uuid4().hex[:8]
    return {
        "username": f"loanuser_{identifier}",
        "email": f"loan_{identifier}@example.com",
        "password": "StrongPass123",
        "phone": "9876543210",
        "monthly_income": 60000,
    }


def create_and_auth():
    user = unique_user()
    reg = client.post("/auth/register", json=user)
    assert reg.status_code == 201
    user_id = reg.json()["id"]
    login = client.post("/auth/login", json={"username": user["username"], "password": user["password"]})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return user_id, {"Authorization": f"Bearer {token}"}


def test_apply_loan_success():
    user_id, headers = create_and_auth()
    payload = {"user_id": user_id, "amount": 10000, "purpose": "personal", "tenure_months": 12, "employment_status": "employed"}

    resp = client.post("/loan/", json=payload, headers=headers)
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["user_id"] == user_id
    assert data["amount"] == 10000


def test_apply_loan_exceeds_limit():
    user_id, headers = create_and_auth()
    payload = {"user_id": user_id, "amount": 1000001, "purpose": "business", "tenure_months": 12, "employment_status": "employed"}
    resp = client.post("/loan/", json=payload, headers=headers)
    assert resp.status_code == 422


def test_apply_when_three_pending_fails():
    user_id, headers = create_and_auth()
    for i in range(3):
        resp = client.post("/loan/", json={"user_id": user_id, "amount": 1000 + i, "purpose": "personal", "tenure_months": 12, "employment_status": "employed"}, headers=headers)
        assert resp.status_code in (200, 201)
    resp = client.post("/loan/", json={"user_id": user_id, "amount": 5000, "purpose": "personal", "tenure_months": 12, "employment_status": "employed"}, headers=headers)
    assert resp.status_code == 422
    assert resp.json()["error"] == "MaxPendingLoansError"


def test_get_my_loans():
    user_id, headers = create_and_auth()
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 15000, "purpose": "education", "tenure_months": 24, "employment_status": "employed"}, headers=headers)
    assert loan_resp.status_code in (200, 201)
    resp = client.get(f"/loan/my/{user_id}", headers=headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_single_loan_detail():
    user_id, headers = create_and_auth()
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 15000, "purpose": "education", "tenure_months": 24, "employment_status": "employed"}, headers=headers)
    assert loan_resp.status_code in (200, 201)
    loan_id = loan_resp.json()["id"]
    resp = client.get(f"/loan/my/{user_id}/loanid/{loan_id}", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == loan_id
    assert body["user_id"] == user_id
