from unittest.mock import patch, Mock
import cli


@patch("cli.requests.get")
def test_get_inventory(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "barcode": "737628064502",
            "product_name": "Organic Almond Milk"
        }
    ]

    mock_get.return_value = mock_response

    response = cli.get_inventory()

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["product_name"] == "Organic Almond Milk"

    mock_get.assert_called_once_with(
        "http://localhost:5000/inventory"
    )


@patch("cli.requests.get")
def test_get_one_item(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk"
    }

    mock_get.return_value = mock_response

    response = cli.requests.get("http://localhost:5000/inventory/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


@patch("cli.requests.post")
def test_post_item(mock_post):
    mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 3,
        "barcode": "123456789",
        "product_name": "Chocolate Bar",
        "brand": "Nestle",
        "ingredients": "Sugar, cocoa, milk",
        "quantity": 10,
        "price": 3.99
    }

    mock_post.return_value = mock_response

    response = cli.requests.post(
        "http://localhost:5000/inventory",
        json={
            "barcode": "123456789",
            "product_name": "Chocolate Bar",
            "brand": "Nestle",
            "ingredients": "Sugar, cocoa, milk",
            "quantity": 10,
            "price": 3.99
        }
    )

    assert response.status_code == 201
    assert response.json()["product_name"] == "Chocolate Bar"


@patch("cli.requests.patch")
def test_patch_item(mock_patch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "quantity": 25
    }

    mock_patch.return_value = mock_response

    response = cli.requests.patch(
        "http://localhost:5000/inventory/1",
        json={"quantity": 25}
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 25


@patch("cli.requests.delete")
def test_delete_item(mock_delete):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Item deleted successfully"
    }

    mock_delete.return_value = mock_response

    response = cli.requests.delete(
        "http://localhost:5000/inventory/2"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"
