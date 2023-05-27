from flask import Blueprint, jsonify, request, current_app
from functools import wraps
import uuid
from repository.task_repo import TaskRepo
from datetime import datetime
from decorator.decorators import authenticate, admin_only

task_controller = Blueprint('task', __name__)

@task_controller.record
def get_task_repo(state):
    # Retrieve the Cassandra Cluster object from the Blueprint's configuration
    cluster = state.app.config['CLUSTER']

    # Create an instance of TaskRepo using the Cluster object
    task_repo = TaskRepo(cluster)

    # Set the task_repo attribute in Flask's application context (g object)
    state.app.config['TASK_REPO'] = task_repo

def with_task_repo(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        task_repo = current_app.config['TASK_REPO']  # Access task_repo from Flask's application configuration
        return f(*args, **kwargs, task_repo=task_repo)  # Pass task_repo as a keyword argument

    return wrapper

# Rest of your code...


@task_controller.route('/tasks', methods=['POST'])
@with_task_repo
@authenticate
def create_task(task_repo):
    try:
        data = request.get_json()
        task_id = uuid.uuid4()
        title = data['title']
        description = data['description']
        status = data['status']
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d %H:%M:%S')
        assigned_user = data['assigned_user']

        task_repo.create_task(task_id, title, description, status, due_date, assigned_user)
        created_task = task_repo.get_task_by_id(task_id)
        return jsonify({'message': 'Task created successfully', 'task': str(created_task)}), 201
    except Exception as e:
        return jsonify({'message': 'Internal error', 'error': str(e)}), 500



@task_controller.route('/tasks', methods=['GET'])
@with_task_repo
@authenticate
def get_all_tasks(task_repo):
    try:
        # Call the TaskRepo methods to handle the requests
        userid = request.args.get('assigned user')
        if userid:
            tasks = task_repo.get_task_by_assigned_userid(userid)
        else:
            tasks = task_repo.get_all_tasks()
        task_list = [task._asdict() for task in tasks]
        return jsonify(task_list), 200
    except Exception as e:
        return jsonify({'message': 'failed to retrieve tasks', 'error': str(e)}), 500
    


@task_controller.route('/tasks/<task_id>', methods=['GET'])
@with_task_repo
@authenticate
def get_task(task_repo, task_id):
    try:
        task = task_repo.get_task_by_id(uuid.UUID(task_id))
        if task:
            return jsonify(task), 200
        else:
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Unable to get task', 'error':str(e)}), 500
    
@task_controller.route('/tasks/<task_id>', methods=['PUT'])
@with_task_repo
@authenticate
def update_task(task_repo, task_id):
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        due_date = data.get('due_date')
        assigned_user = data.get('assigned_user')
        task_repo.update_task(uuid.UUID(task_id), title, description, status, due_date, assigned_user)
        updated_task = task_repo.get_task_by_id(uuid.UUID(task_id))
        return jsonify({'message': 'Task updated successfully', 'task': str(updated_task)}), 200
    except Exception as e:
        return jsonify({'message': 'update failed', 'error':str(e)}), 500

@task_controller.route('/tasks/<task_id>', methods=['DELETE'])
@with_task_repo
@authenticate
def delete_task(task_repo, task_id):
    try:
        task_repo.delete_task(uuid.UUID(task_id))
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Task deletion failed', 'error': str(e)}), 500

@task_controller.route('/tasks/filter', methods=['GET'])
@with_task_repo
@authenticate    
def filter_tasks(task_repo):
    try:
        status = request.args.get('status')
        due_date = request.args.get('due_date')
        assigned_user = request.args.get('assigned_user')

        result = task_repo.filter_tasks(status, due_date, assigned_user)
        if not result:
            return jsonify({'message': 'empty result'}), 200
        serialized_result = []

        for row in result:
            serialized_row = {}
            for index, value in enumerate(row):
                serialized_row[row._fields[index]] = value
            serialized_result.append(serialized_row)
        return jsonify(serialized_result), 200
        
                
    except Exception as e:
        return jsonify({'message': 'internal error', 'Error': str(e)}), 400


@task_controller.route('/tasks/<task_id>', methods=['PUT'])
@with_task_repo
@authenticate
@admin_only
def assign_task(task_repo, task_id):
    try:
        assigned_user = request.args.get('assigned_user')
        task_repo.update_task(task_id=uuid.UUID(task_id), assigned_user= assigned_user)
        updated_task = task_repo.get_task_by_id(uuid.UUID(task_id))
        return jsonify({'message': 'user assigned successfully', 'task info':str(updated_task)}), 200
    except Exception as e:
        return jsonify({'message': 'user assigned failed', 'task info':str(e)}), 400



def shutdown_session(e=None):
    task_controller.task_repo.close_session()



