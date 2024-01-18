from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data (replace this with a database in a real-world scenario)
tasks = [
    {"id": 1, "title": "Task 1", "description": "Description 1", "due_date": "2024-01-31"},
    {"id": 2, "title": "Task 2", "description": "Description 2", "due_date": "2024-02-15"},
]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json or 'due_date' not in request.json:
        return jsonify({'error': 'Title and due_date are required'}), 400

    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'due_date': request.json['due_date'],
    }

    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['due_date'] = request.json.get('due_date', task['due_date'])
    return jsonify({'task': task})

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
