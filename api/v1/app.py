#!/usr/bin/python3
"""This script starts an API"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import environ
app = Flask(__name__)


app.register_blueprint(app_views)
@app.teardown_appcontext
def teardown(exception):
    """Closes the storage session"""
    storage.close()


@app.errorhandler(404)
def handle_err(err):
    """This method handles error pages"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    ip = environ['HBNB_API_HOST']
    port = environ['HBNB_API_PORT']
    app.run(host=ip, port=port, threaded=True, debug=True)
