import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Task
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- Database Configuration ---
# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Create an 'instance' folder if it doesn't exist
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)
# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize App and DB ---
db.init_app(app)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to prevent caching.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0, no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# --- API Endpoints ---

# [GET] All Tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed,
        'category': task.category,
        'client_name': task.client_name,
        'location': task.location
    } for task in tasks])

# [POST] Create Task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=due_date,
        category=data.get('category', '工作'),
        client_name=data.get('client_name'),
        location=data.get('location')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'title': new_task.title}), 201

# [GET] Single Task
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed,
        'category': task.category,
        'client_name': task.client_name,
        'location': task.location
    })

# [PUT] Update Task
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    if 'due_date' in data:
        task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    task.completed = data.get('completed', task.completed)
    task.category = data.get('category', task.category)
    task.client_name = data.get('client_name', task.client_name)
    task.location = data.get('location', task.location)

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

# [DELETE] Delete Task
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

# [GET] Tasks for Board View
@app.route('/api/tasks/board', methods=['GET'])
def get_board_tasks():
    from datetime import date, timedelta

    today = date.today()
    end_of_week = today + timedelta(days=6 - today.weekday())
    end_of_next_week = end_of_week + timedelta(days=7)

    tasks = Task.query.filter(Task.completed == False).all()
    
    board_tasks = {
        'today': [],
        'this_week': [],
        'future': []
    }

    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed,
            'category': task.category,
            'client_name': task.client_name,
            'location': task.location
        }
        if task.due_date:
            task_due_date = task.due_date.date()
            if task_due_date == today:
                board_tasks['today'].append(task_data)
            elif today < task_due_date <= end_of_week:
                board_tasks['this_week'].append(task_data)
            else:
                board_tasks['future'].append(task_data)
        else:
            board_tasks['future'].append(task_data)

    return jsonify(board_tasks)

# [GET] Tasks for Calendar View
@app.route('/api/tasks/calendar', methods=['GET'])
def get_calendar_tasks():
    tasks = Task.query.filter(Task.due_date.isnot(None)).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'start': task.due_date.isoformat(),
        'allDay': True # Or determine based on task properties
    } for task in tasks])

# --- CLI Command to initialize the database ---
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    with app.app_context():
        db.create_all()
    print("Initialized the database.")

@app.cli.command("reset-db")
def reset_db_command():
    """Destroys and recreates the database with fresh data."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Add some fresh test data
        from datetime import date, timedelta
        today = date.today()
        task1 = Task(title="Fresh Task for Today", due_date=datetime.combine(today, datetime.min.time()))
        task2 = Task(title="Fresh Task for This Week", due_date=datetime.combine(today + timedelta(days=3), datetime.min.time()))
        task3 = Task(title="Fresh Task with No Due Date")
        db.session.add_all([task1, task2, task3])
        db.session.commit()
    print("Database has been reset and seeded.")

if __name__ == '__main__':
    app.run(debug=True)
