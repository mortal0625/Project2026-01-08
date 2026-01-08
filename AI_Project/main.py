from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Define the path for the JSON file
TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    tasks = load_tasks()
    if request.method == 'GET':
        # Sort tasks by date, tasks without a date can be put at the end
        sorted_tasks = sorted(tasks, key=lambda x: x.get('date', '9999-12-31'))
        return jsonify(sorted_tasks)
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'error': 'Missing description'}), 400
        
        new_task = {
            'id': len(tasks) + 1,
            'description': data['description'],
            'completed': False,
            'date': data.get('date'), # Accept an optional date
            'status': data.get('status', 'todo') # Default status to 'todo'
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Missing status'}), 400

    task['status'] = data['status']
    save_tasks(tasks)
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    task_to_delete = next((t for t in tasks if t.get('id') == task_id), None)
    
    if not task_to_delete:
        return jsonify({'error': 'Task not found'}), 404

    tasks = [t for t in tasks if t.get('id') != task_id]
    save_tasks(tasks)
    
    return jsonify({'message': 'Task deleted successfully'}), 200

if __name__ == '__main__':
    # Note: The port for the backend is 5000
    app.run(debug=True, port=5000)
        