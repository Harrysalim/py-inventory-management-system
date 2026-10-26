from flask import Flask, jsonify, request
from inventory import inventory
import requests

app = Flask(__name__)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):

    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item:
        return jsonify(item), 200

    return jsonify({
        "error": "Item not found"
    }), 404

@app.route('/inventory', methods=['POST'])
def add_item():

    data = request.get_json()

    new_item = {
        "id": inventory[-1]["id"] + 1,
        "barcode": data["barcode"],
        "product_name": data["product_name"],
        "brand": data["brand"],
        "ingredients": data["ingredients"],
        "quantity": data["quantity"],
        "price": data["price"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):

    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if not item:
        return jsonify({
            "error": "Item not found"
        }), 404

    data = request.get_json()

    item.update(data)

    return jsonify(item), 200

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):

    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if not item:
        return jsonify({
            "error": "Item not found"
        }), 404

    inventory.remove(item)

    return jsonify({
        "message": "Item deleted successfully"
    }), 200

def fetch_product_data(barcode):

    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    try:
        data = response.json()
    except Exception as e:
        print("JSON Error:", e)
        print(response.text[:500])
        return None

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name", "Unknown"),
        "brand": product.get("brands", "Unknown"),
        "ingredients": product.get("ingredients_text", "No ingredients found")
    }

@app.route('/product/<barcode>', methods=['GET'])
def get_product(barcode):

    product = fetch_product_data(barcode)

    if not product:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200

if __name__ == "__main__":
    app.run(debug=True)

//finalized the summative lab
