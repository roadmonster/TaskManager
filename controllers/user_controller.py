from flask import Blueprint, jsonify, request, current_app
from repository.user_repo import UserRepo
from functools import wraps
import uuid
from decorator.decorators import authenticate
user_controller = Blueprint('user', __name__)

@user_controller.record
def get_user_repo(state):
    cluster = state.app.config['CLUSTER']
    user_repo = UserRepo(cluster)
    state.app.config['USER_REPO'] = user_repo

def with_user_repo(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user_repo = current_app.config['USER_REPO']  # Access task_repo from Flask's application configuration
        return f(*args, **kwargs, user_repo=user_repo)  # Pass task_repo as a keyword argument

    return wrapper

@user_controller.route('/users', methods=['POST'])
@with_user_repo
@authenticate
def create_user(user_repo):
    data = request.get_json()
    user_id = uuid.uuid4()
    username = data['username']
    passoword = data['password']
    email = data['email']
    additional_info = data['additional_info']

    user_repo.create_user(user_id, username, passoword, email, additional_info)
    user_id_str = str(user_id)
    return jsonify({'message': f'User created{user_id_str}'})

@user_controller.route('/users/<user_id>', methods=['GET'])
@with_user_repo
@authenticate
def get_user_by_userid(user_repo, user_id):
    user = user_repo.get_user_by_userid(uuid.UUID(user_id))
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'user not exist'})

@user_controller.route('/users', methods=['GET'])
@with_user_repo
@authenticate
def get_all_users(user_repo):
    users = user_repo.get_all_users()
    serialized_users = []
    for row in users:
        serialized_row = {}
        for i, value in enumerate(row):
            serialized_row[row._fields[i]] = value
        serialized_users.append(serialized_row)
    
    return jsonify(serialized_users), 200
    



    






