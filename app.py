from flask import Flask, current_app
from controllers.task_controller_v2 import task_controller
from cassandra.cluster import Cluster
from controllers.user_controller import user_controller
from controllers.log_in_out_controller import log_in_out_controller

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Configure the Cassandra Cluster object
# Set the Cluster object in the Blueprint's configuration
app.config['CLUSTER'] = Cluster(['localhost'])

# Create an application context
with app.app_context():
    # Register the task_controller Blueprint
    app.register_blueprint(task_controller)

    app.register_blueprint(user_controller)

    app.register_blueprint(log_in_out_controller)

# @app.teardown_appcontext
# def shutdown_task_controller(error=None):
#     task_repo = current_app.config.get('TASK_REPO')
#     if task_repo is not None:
#         task_repo.close_session()

#     user_repo = current_app.config.get('USER_REPO')
#     if user_repo is not None:
#         user_repo.close_session()
#     app.config['CLUSTER'].shutdown()


if __name__ == '__main__':
    app.run(debug=True)
