from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_products_returns_ok():
    response = client.get("/products")
    assert response.status_code == 200


def test_post_then_get_returns_created_product():
    payload = {"name": "Test Product", "description": "A product for testing", "price": 19.99}

    post_response = client.post("/products", json=payload)
    assert post_response.status_code == 201
    created = post_response.json()

    get_response = client.get(f"/products/{created['id']}")
    assert get_response.status_code == 200


def test_get_unknown_product_returns_not_found():
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_post_invalid_product_returns_bad_request():
    payload = {"name": "", "description": "Missing name", "price": 10}
    response = client.post("/products", json=payload)
    assert response.status_code == 400


def test_delete_product_returns_no_content():
    payload = {"name": "Temp Product", "description": "Will be deleted", "price": 5}
    post_response = client.post("/products", json=payload)
    created = post_response.json()

    delete_response = client.delete(f"/products/{created['id']}")
    assert delete_response.status_code == 204
