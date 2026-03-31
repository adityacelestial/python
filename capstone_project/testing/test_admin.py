import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def unique_user(role="user"):
    identifier = uuid.uuid4().hex[:8]
    user = {
        "username": f"{role}_user_{identifier}",
        "email": f"{role}_{identifier}@example.com",
        "password": "StrongPass123",
        "phone": "9876543210",
        "monthly_income": 70000,
    }
    if role == "admin":
        user["role"] = "admin"
    return user


def auth_user(role="user"):
    u = unique_user(role)
    resp = client.post("/auth/register", json=u)
    assert resp.status_code == 201
    login = client.post("/auth/login", json={"username": u["username"], "password": u["password"]})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return resp.json()["id"], {"Authorization": f"Bearer {token}"}


def test_admin_views_all_loans():
    user_id, user_headers = auth_user("user")
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 20000, "purpose": "home", "tenure_months": 36, "employment_status": "employed"}, headers=user_headers)
    assert loan_resp.status_code in (200, 201)

    admin_id, admin_headers = auth_user("admin")
    resp = client.get("/admin/loans", headers=admin_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_admin_approves_loan():
    user_id, user_headers = auth_user("user")
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 25000, "purpose": "business", "tenure_months": 24, "employment_status": "self_employed"}, headers=user_headers)
    loan_id = loan_resp.json()["id"]

    admin_id, admin_headers = auth_user("admin")
    resp = client.patch(f"/admin/loans/{loan_id}/review", json={"status": "approved", "admin_remarks": "Good credit"}, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "approved"


def test_admin_rejects_loan():
    user_id, user_headers = auth_user("user")
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 30000, "purpose": "vehicle", "tenure_months": 18, "employment_status": "employed"}, headers=user_headers)
    loan_id = loan_resp.json()["id"]

    admin_id, admin_headers = auth_user("admin")
    resp = client.patch(f"/admin/loans/{loan_id}/review", json={"status": "rejected", "admin_remarks": "Low income"}, headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"


def test_admin_rereview_already_reviewed_loan():
    user_id, user_headers = auth_user("user")
    loan_resp = client.post("/loan/", json={"user_id": user_id, "amount": 15000, "purpose": "education", "tenure_months": 24, "employment_status": "student"}, headers=user_headers)
    loan_id = loan_resp.json()["id"]

    admin_id, admin_headers = auth_user("admin")
    first = client.patch(f"/admin/loans/{loan_id}/review", json={"status": "approved", "admin_remarks": "Ok"}, headers=admin_headers)
    assert first.status_code == 200

    second = client.patch(f"/admin/loans/{loan_id}/review", json={"status": "rejected", "admin_remarks": "Second check"}, headers=admin_headers)
    assert second.status_code == 422
    assert second.json()["error"] == "InvalidLoanReviewError"


def test_non_admin_cannot_access_admin():
    user_id, user_headers = auth_user("user")
    resp = client.get("/admin/loans", headers=user_headers)
    assert resp.status_code == 403
    assert resp.json()["error"] == "ForbiddenError"
