import requests

BASE_URL = "http://localhost:5000"


def get_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    print("GET:", response.status_code)
    print(response.json())

    return response


def get_one_item():
    response = requests.get(f"{BASE_URL}/inventory/1")

    print("\nGET ONE:", response.status_code)
    print(response.json())

    return response


def post_item():
    response = requests.post(
        f"{BASE_URL}/inventory",
        json={
            "barcode": "123456789",
            "product_name": "Chocolate Bar",
            "brand": "Nestle",
            "ingredients": "Sugar, cocoa, milk",
            "quantity": 10,
            "price": 3.99
        }
    )

    print("\nPOST:", response.status_code)
    print(response.json())

    return response


def patch_item():
    response = requests.patch(
        f"{BASE_URL}/inventory/1",
        json={
            "quantity": 25
        }
    )

    print("\nPATCH:", response.status_code)
    print(response.json())

    return response


def delete_item():
    response = requests.delete(
        f"{BASE_URL}/inventory/2"
    )

    print("\nDELETE:", response.status_code)
    print(response.json())

    return response


if __name__ == "__main__":
    get_inventory()
    get_one_item()
    post_item()
    patch_item()
    delete_item()


