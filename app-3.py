from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ------------------------------
# Task3: New Model with Relationship
# ------------------------------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    # One-to-many relationship: one category has many tasks
    tasks = db.relationship('Task', backref='category', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    priority = db.Column(db.String(20))
    due_date = db.Column(db.String(50))
    completed = db.Column(db.Boolean, default=False)
    # Foreign key to Category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

# ------------------------------
# Task2: Extract Endpoint (English version)
# ------------------------------
@app.route('/api/extract', methods=['POST'])
def extract():
    data = request.get_json()
    text = data.get('text', '')
    lines = text.split('\n')
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        results.append({
            "title": line,
            "priority": "normal",
            "due_date": "unknown"
        })
    return jsonify({
        "success": True,
        "extracted_count": len(results),
        "data": results
    })

# ------------------------------
# Task3: Category & Task with Relationship Endpoints
# ------------------------------
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({
        "id": category.id,
        "name": category.name
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        title=data['title'],
        priority=data.get('priority', 'normal'),
        due_date=data.get('due_date', 'unknown'),
        category_id=data.get('category_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "priority": task.priority,
        "due_date": task.due_date,
        "category_id": task.category_id
    })

# ------------------------------
# For Task4: Pagination + Sorting Example
# ------------------------------
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')

    query = Task.query
    if order == 'desc':
        query = query.order_by(getattr(Task, sort_by).desc())
    else:
        query = query.order_by(getattr(Task, sort_by))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "success": True,
        "data": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority,
                "due_date": t.due_date,
                "completed": t.completed,
                "category_id": t.category_id
            } for t in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total
        }
    })

# Create tables (run once)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)