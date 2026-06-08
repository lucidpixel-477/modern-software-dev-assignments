from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# === Task 3: Models with Relationship ===
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='category', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default="medium")
    due_date = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

# === Task 2: Extraction Endpoint ===
@app.route('/api/extract', methods=['POST'])
def extract_action_items():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"success": False, "error": "Missing text"}), 400

    text = data["text"]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    items = [{"title": line, "priority": "medium", "due_date": None} for line in lines]
    return jsonify({"success": True, "count": len(items), "data": items})

# === Task 3: Category & Task APIs ===
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.json
    cat = Category(name=data["name"])
    db.session.add(cat)
    db.session.commit()
    return jsonify({"id": cat.id, "name": cat.name})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(
        title=data["title"],
        priority=data.get("priority"),
        due_date=data.get("due_date"),
        category_id=data.get("category_id")
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "category_id": task.category_id})

# === TASK 4: PAGINATION & SORTING (ºËÐÄÍê³É) ===
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 3, type=int)
    sort_by = request.args.get("sort_by", "id")
    order = request.args.get("order", "asc")

    query = Task.query

    # Sorting
    if sort_by == "priority":
        query = query.order_by(Task.priority.desc() if order == "desc" else Task.priority)
    elif sort_by == "due_date":
        query = query.order_by(Task.due_date.desc() if order == "desc" else Task.due_date)
    else:
        query = query.order_by(Task.id.desc() if order == "desc" else Task.id)

    # Pagination
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total": paginated.total,
        "total_pages": paginated.pages,
        "data": [{
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "due_date": t.due_date,
            "completed": t.completed,
            "category_id": t.category_id
        } for t in paginated.items]
    })

# Create DB tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)