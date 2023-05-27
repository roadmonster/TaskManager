from functools import wraps
from flask import jsonify, session

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in
        if 'username' not in session:
            return jsonify({'message': 'Unauthorized access'}), 401
        return func(*args, **kwargs)
    return wrapper

# Admin authentication decorator
def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in as admin
        if session.get('username') != 'admin':
            return jsonify({'message': 'Unauthorized access'}), 401
        return func(*args, **kwargs)
    return wrapper