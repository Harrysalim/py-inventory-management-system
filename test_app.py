import pytest
from app import app
from inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) >= 1


def test_get_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Organic Almond Milk"


def test_get_item_not_found(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"


def test_add_item(client):
    new_item = {
        "barcode": "123456789",
        "product_name": "Chocolate Bar",
        "brand": "Nestle",
        "ingredients": "Sugar, cocoa, milk",
        "quantity": 10,
        "price": 3.99
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201

    data = response.get_json()

    assert data["product_name"] == "Chocolate Bar"
    assert data["brand"] == "Nestle"
    assert data["quantity"] == 10
    assert data["price"] == 3.99


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={"quantity": 25}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["quantity"] == 25


def test_update_item_not_found(client):
    response = client.patch(
        "/inventory/999",
        json={"quantity": 25}
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"


def test_delete_item(client):
    new_item = {
        "barcode": "987654321",
        "product_name": "Test Product",
        "brand": "Test Brand",
        "ingredients": "Test ingredients",
        "quantity": 5,
        "price": 2.99
    }

    post_response = client.post("/inventory", json=new_item)

    assert post_response.status_code == 201

    item_id = post_response.get_json()["id"]

    response = client.delete(f"/inventory/{item_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Item deleted successfully"


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Item not found"
