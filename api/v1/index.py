#!/usr/bin/python3
"""This script defines a route status"""
from api.v1.views import app_views


@app_views.route('/status')
@app_views.route('/')
def status():
    """Request status"""
    return {"status": "OK"}
