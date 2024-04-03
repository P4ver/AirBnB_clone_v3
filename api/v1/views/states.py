#!/usr/bin/python3
'''
Creates sts app,
'''
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False)
def get_Allstates():
    """display the states and cities listed in alphabetical order"""
    states = storage.all(State).values()
    states_list = [State.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id):
    """display the states and cities listed in alphabetical order"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """display the states and cities listed in alphabetical order"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """display the states and cities listed in alphabetical order"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(404, 'No JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(404, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """display the states and cities listed in alphabetical order"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(404, 'No JSON')
        data = request.get_json()
        ignorekey = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignorekey:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
