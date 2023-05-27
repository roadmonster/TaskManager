from flask import jsonify, session, request, Blueprint
from decorator.decorators import authenticate
log_in_out_controller = Blueprint('loginout', __name__)


@log_in_out_controller.route('/login', methods=['POST'])
def login():
    try:
        # Extract username and password from the request body
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Perform user authentication (example logic)
        if username == 'admin' and password == 'admin123':
            # Store username in session
            session['username'] = username
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'message': 'Failed to login', 'error': str(e)}), 500
    

@log_in_out_controller.route('/logout', methods=['POST'])
@authenticate
def logout():
    try:
        # Clear the session
        session.clear()
        return jsonify({'message': 'Logged out successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to logout', 'error': str(e)}), 500


