"""
Flask Application for Kubernetes CI/CD Assignment
This module implements a simple Flask web application
that serves as a demonstration of containerized deployment.
"""
from flask import Flask

# Initialize Flask application instance
flask_application = Flask(__name__)


@flask_application.route('/')
def home_endpoint():
    """
    Root endpoint that returns a greeting message.
    Returns:
        str: A simple greeting string
    """
    return 'Hello, World!'


@flask_application.route('/health')
def health_check():
    """
    Health check endpoint for Kubernetes probes.
    Returns:
        str: Status message indicating service health
    """
    return 'OK', 200


if __name__ == '__main__':
    # Run application on all interfaces, port 5000
    flask_application.run(host='0.0.0.0', port=5000, debug=False)
