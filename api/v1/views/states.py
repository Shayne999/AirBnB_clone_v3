#!/usr/bin/python3

""" Create a new view for State objects that handles
all default RESTFul API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views, storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Fetches then returns all state objects as a JSON response """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)

@app_views.route('/states', methods=[POST], strict_slashes=False)
def create_state():
    """ Creates state route """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ Gets a state using the state's ID """
    new_obj = storage.get("State", str(state_id))

    if new_obj is None:
        abort(404)

    return jsonify(new_obj.to_json())

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """ Returns the State object with the status code 200 """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')

    new_obj = storage.get('State', str(state_id))

    if new_obj is None:
        abort(400)

    for key, val in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_obj, key, val)
    new_obj.save()
    return jsonify(new_obj.to_json())

@app_views.route('/state/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state_by_id(state_id):
    """ Deletes a state by Id """
    new_obj = storage.get('State', str(state_id))

    if new_obj is None:
        abort(404)

    storage.delete(new_obj)
    storage.save()

    return jsonify({})
