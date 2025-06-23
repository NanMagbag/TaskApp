from flask import Flask, request, jsonify
from models import db, User, Task, CalendarEvent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"message": "TaskPal API is running!"})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/tasks/<int:user_id>', methods=['GET', 'POST'])
def tasks(user_id):
    if request.method == 'POST':
        data = request.json
        task = Task(
            user_id=user_id,
            title=data['title'],
            description=data.get('description'),
            due_date=data['due_date'],
            due_time=data.get('due_time'),
            status=data['status'],
            progress=data.get('progress', 0)
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task created"}), 201

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "due_date": t.due_date,
        "due_time": t.due_time,
        "status": t.status,
        "progress": t.progress
    } for t in tasks])

@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def update_delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'PUT':
        data = request.json
        task.title = data['title']
        task.description = data['description']
        task.due_date = data['due_date']
        task.due_time = data['due_time']
        task.status = data['status']
        task.progress = data['progress']
        db.session.commit()
        return jsonify({"message": "Task updated"})

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

@app.route('/calendar/<int:user_id>', methods=['GET', 'POST'])
def calendar(user_id):
    if request.method == 'POST':
        data = request.json
        event = CalendarEvent(
            user_id=user_id,
            title=data['title'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            date=data['date']
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created"}), 201

    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": e.id,
        "title": e.title,
        "date": e.date,
        "start_time": e.start_time,
        "end_time": e.end_time
    } for e in events])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
