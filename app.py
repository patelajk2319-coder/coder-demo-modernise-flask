import json
from pathlib import Path

from flask import Flask, abort, jsonify, request

DATA_FILE = Path(__file__).parent / "data.json"

app = Flask(__name__)


def load_items():
    with DATA_FILE.open() as f:
        return json.load(f)


def save_items(items):
    with DATA_FILE.open("w") as f:
        json.dump(items, f)


ITEMS = load_items()


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(ITEMS)


@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    item_id = int(item_id)
    for item in ITEMS:
        if item["id"] == item_id:
            return jsonify(item)
    abort(404)


@app.route("/items", methods=["POST"])
def create_item():
    body = request.get_json()
    if not body or "name" not in body or "quantity" not in body:
        abort(400)

    new_id = max((item["id"] for item in ITEMS), default=0) + 1
    item = {"id": new_id, "name": body["name"], "quantity": body["quantity"]}
    ITEMS.append(item)
    save_items(ITEMS)
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
