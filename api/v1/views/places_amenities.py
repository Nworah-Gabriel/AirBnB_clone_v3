#!/usr/bin/python3
""" Module for amenity object view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_of_place(place_id):
    """ Returns all amenity objects of a certain place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenities_dict_list = [amenity.to_dict() for amenity in
                           place.amenities]
    return jsonify(amenities_dict_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_of_place(place_id, amenity_id):
    """ Method deletes amenity object of a certain place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity or amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """ Method adds an amenity object to a place """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
