#!/usr/bin/python3
"""User file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.city import City
from models import storage
from api.v1.app import handle_err


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def users(city_id):
    """ This method request for users. """
    cities = storage.all(City).values()
    city_nedded = [city for city in cities if city.id == city_id]
    return jsonify([item.to_dict() for item in city_nedded.places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def places_id(place_id):
    """ This method filters the places by id. """
    places = storage.all(Place).values()
    obj = [item for item in places if item.id == place_id]
    if obj:
        return jsonify(obj[0].to_dict())
    return handle_err('err')


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def placesDelete(user_id):
    """ This method deletes a place by id """
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return handle_err('err')


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def placesPost():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'user_id' not in req:
            return "Missing user_id", 400
        if 'name' not in req:
            return "Missing name", 400
        new_obj = Place()
        for key, value in req.items():
            setattr(new_obj, key, value)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def placesPut(user_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(Place, place_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return handle_err('err')
    except:
        return "Not a JSON\n", 400
