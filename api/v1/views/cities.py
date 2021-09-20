#!/usr/bin/python3
"""City file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models.city import City
from models import storage
from api.v1.app import handle_err


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """ This method request for cities. """
    states = storage.all(State).values()
    needed_state = [state for state in states if state.id == state_id]
    if needed_state:
        return jsonify([item.to_dict() for item in needed_state[0].cities])
    return handle_err('err')


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_id(city_id):
    """ his method filters the city by id. """
    cities = storage.all(City).values()
    obj = [item for item in cities if item.id == city_id]
    if obj:
        return jsonify(obj[0].to_dict())
    return handle_err('err')


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id):
    """ This method deletes a city by id. """
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return handle_err('err')


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def cities_create():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'name' not in req:
            return "Missing name\n", 400
        new_obj = City(state_id=state_id, name=req['name'])
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def cities_update(city_id):
    """ This method update an object. """
    try:
        req = request.get_json()
        obj = storage.get(City, city_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return handle_err('err')
    except:
        return "Not a JSON\n", 400
