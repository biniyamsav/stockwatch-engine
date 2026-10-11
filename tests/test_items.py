from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_nonexistent_item():
    response = client.get("/api/v1/items/999999")

    assert response.status_code == 404

def test_create_item(client):
    response = client.post(
        "/api/v1/items",
        json={
            "name": "Test Keyboard",
            "sku": "TEST-KEY-003",
            "quantity": 10,
            "low_stock_threshold": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Test Keyboard"
    assert data["sku"] == "TEST-KEY-003"
    assert data["quantity"] == 10
