#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, url_for, make_response, jsonify
from flask_cors import cross_origin, CORS
from flasgger import Swagger
from flasgger.utils import swag_from
import os
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
swagger = Swagger(app)
app.url_map.strict_slashes = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
host = os.getenv('HBNB_API_HOST', '35.237.240.179')
port = os.getenv('HBNB_API_PORT', 5000)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """ Method calls .Close current SQLAchemy Session """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        description: a resource was not found
    """
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
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
