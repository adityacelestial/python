from fastapi.testclient import TestClient

from main import app


client=TestClient(app)

def health_check():
    response=client.get("/health")
    
    assert response.status_code==200
    
# def test_create_user():
    
#     response=client.post("/auth/register",json={
#   "username": "aditya_review4",
#   "email": "adityaereview4@example.com",
#   "password": "StrongPass123",
#   "phone": "9876543210",
#   "monthly_income": 50000
# })
    
#     assert response.status_code==200
    
#     assert response.json()=={
#     "id": 14,
#     "username": "aditya_review4",
#     "email": "adityaereview4@example.com",
#     "phone": "9876543210",
#     "monthly_income": 50000,
#     "role": "user",
#     "is_active": "true",
#     "created_at": "2026-03-27T16:36:43.056333"
# }
    
def get_loan_by_user_id():
    response=client.get("/loan/my/2")
    assert response.status_code==200
    
    assert response.json()==[
    {
        "id": "4",
        "user_id": "9",
        "amount": "10000",
        "purpose": "personal",
        "tenure_months": 6,
        "status": "pending",
        "admin_remarks": "null",
        "reviewed_by": "null",
        "reviewed_at": "null",
        "applied_at": "2026-03-27T15:09:02.751969"
    },
    {
        "id": "5",
        "user_id": "9",
        "amount": "100000",
        "purpose": "education",
        "tenure_months": "6",
        "status": "pending",
        "admin_remarks": "null",
        "reviewed_by": "null",
        "reviewed_at": "null",
        "applied_at": "2026-03-27T15:09:02.751969"
    }
]