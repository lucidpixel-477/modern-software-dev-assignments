from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
action_items = [
    {"id": 1, "title": "Finish homework", "completed": False},
    {"id": 2, "title": "Run review", "completed": False}
]

# Get all items
@app.route("/api/action-items", methods=["GET"])
def get_all_items():
    try:
        return jsonify({
            "success": True,
            "data": action_items
        })
    except Exception as e:
        return jsonify({"success": False, "error": "Server error"}), 500

# Get single item by ID
@app.route("/api/action-items/<int:item_id>", methods=["GET"])
def get_single_item(item_id):
    if item_id <= 0:
        return jsonify({"success": False, "error": "Invalid ID"}), 400

    item = next((i for i in action_items if i["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404

    return jsonify({"success": True, "data": item})

# Delete an item
@app.route("/api/action-items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global action_items
    if item_id <= 0:
        return jsonify({"success": False, "error": "Invalid ID"}), 400

    original_count = len(action_items)
    action_items = [i for i in action_items if i["id"] != item_id]

    if len(action_items) == original_count:
        return jsonify({"success": False, "error": "Item not found"}), 404

    return jsonify({"success": True, "message": "Item deleted"})

if __name__ == "__main__":
    app.run(debug=True)