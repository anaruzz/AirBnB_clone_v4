#!/usr/bin/python3
"""
Flask App that integrates with AirBnB HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """
    handles 400 errros
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):

    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    HTTPException function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    setup_global_errors()
    app.run(host=host, port=port)
