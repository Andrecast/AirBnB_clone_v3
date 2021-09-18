#!/usr/bin/python3
"""Reviews file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models import storage
from api.v1.app import handle_err


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """ This method request for reviews. """
    reviews = storage.all(Review).values()
    place_nedded = [place for place in reviews if place.id == place_id]
    return jsonify([item.to_dict() for item in place_nedded.reviews])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def reviews_id(review_id):
    """ This method filters the reviews by id. """
    reviews = storage.all(Review).values()
    obj = [item for item in reviews if item.id == review_id]
    if obj:
        return jsonify(obj[0].to_dict())
    return handle_err('err')


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def reviewDelete(user_id):
    """ This method deletes a place by id """
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return handle_err('err')


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def reviewsPost():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'user_id' not in req:
            return "Missing user_id", 400
        if 'text' not in req:
            return "Missing text", 400
        new_obj = Place()
        for key, value in req.items():
            setattr(new_obj, key, value)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def reviewsPut(user_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(Review, review_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return handle_err('err')
    except:
        return "Not a JSON\n", 400
