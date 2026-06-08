from flask import Flask, jsonify, request
import re

app = Flask(__name__)

# -------------------- In-memory "database" --------------------
action_items = [
    {"id": 1, "title": "Finish homework", "completed": False, "priority": "medium", "due_date": None},
    {"id": 2, "title": "Run review", "completed": False, "priority": "medium", "due_date": None}
]
next_id = 3

# -------------------- Task 1: Endpoints & Validation --------------------
@app.route("/api/action-items", methods=["GET"])
def get_all_items():
    return jsonify({"success": True, "data": action_items})

@app.route("/api/action-items/<int:item_id>", methods=["GET"])
def get_single_item(item_id):
    if item_id <= 0:
        return jsonify({"success": False, "error": "Invalid ID"}), 400
    item = next((i for i in action_items if i["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404
    return jsonify({"success": True, "data": item})

@app.route("/api/action-items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global action_items
    if item_id <= 0:
        return jsonify({"success": False, "error": "Invalid ID"}), 400
    original_length = len(action_items)
    action_items = [i for i in action_items if i["id"] != item_id]
    if len(action_items) == original_length:
        return jsonify({"success": False, "error": "Item not found"}), 404
    return jsonify({"success": True, "message": "Deleted successfully"})

# -------------------- Task 2: Enhanced Extraction Logic --------------------
# Regex patterns for action verbs, due dates, and priorities
ACTION_VERBS = r"(do|review|schedule|call|send|finish|prepare|check|meet|update|submit|complete|fix|implement)"
TIME_PATTERN = r"(by\s+|on\s+)?(today|tomorrow|next\s+week|eod|morning|afternoon|evening|\d{4}-\d{2}-\d{2})"
PRIORITY_PATTERN = r"(urgent|high|medium|low)"

action_item_pattern = re.compile(
    rf"^\s*({ACTION_VERBS})\s+(.*?)\s*({TIME_PATTERN})?\s*({PRIORITY_PATTERN})?\s*[.!]?$",
    re.IGNORECASE
)

def extract_action_items(text):
    """
    Enhanced action item extraction with pattern matching,
    duplicate detection, priority, and due date parsing.
    """
    lines = text.splitlines()
    extracted = []
    seen_titles = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = action_item_pattern.match(line)
        if not match:
            continue

        verb = match.group(1).lower()
        title = match.group(2).strip()
        due_date = match.group(3).strip() if match.group(3) else None
        priority = match.group(5).lower() if match.group(5) else "medium"

        # Deduplicate by title
        if title in seen_titles:
            continue
        seen_titles.add(title)

        extracted.append({
            "title": title,
            "priority": priority,
            "due_date": due_date
        })

    return extracted

@app.route("/api/extract", methods=["POST"])
def extract():
    global next_id
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"success": False, "error": "Missing 'text' field"}), 400

    text = data["text"]
    items = extract_action_items(text)

    added_items = []
    for item in items:
        new_item = {
            "id": next_id,
            "title": item["title"],
            "completed": False,
            "priority": item["priority"],
            "due_date": item["due_date"]
        }
        action_items.append(new_item)
        added_items.append(new_item)
        next_id += 1

    return jsonify({
        "success": True,
        "extracted_count": len(added_items),
        "data": added_items
    })

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True)