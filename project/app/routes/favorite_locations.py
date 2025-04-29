from flask import Blueprint, request, jsonify, session
from app.models.favorite_location import favorite_locations_model

favorite_locations_bp = Blueprint('favorite_locations', __name__)

# Helper: require login
def require_login():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401

@favorite_locations_bp.route('/locations', methods=['POST'])
def add_location():
    auth = require_login()
    if auth:
        return auth
    data = request.get_json()
    name = data.get('name')
    lat = data.get('lat')
    lng = data.get('lng')
    description = data.get('description', '')
    if not all([name, lat, lng]):
        return jsonify({'error': 'Name, lat, and lng required'}), 400
    loc = favorite_locations_model.add_location(name, lat, lng, description, session['username'])
    return jsonify({'id': loc.loc_id, 'name': loc.name, 'lat': loc.lat, 'lng': loc.lng, 'description': loc.description}), 201

@favorite_locations_bp.route('/locations', methods=['GET'])
def list_locations():
    auth = require_login()
    if auth:
        return auth
    locations = favorite_locations_model.get_all_locations(user=session['username'])
    return jsonify([
        {'id': l.loc_id, 'name': l.name, 'lat': l.lat, 'lng': l.lng, 'description': l.description}
        for l in locations
    ])

@favorite_locations_bp.route('/locations/<int:loc_id>', methods=['GET'])
def get_location(loc_id):
    auth = require_login()
    if auth:
        return auth
    loc = favorite_locations_model.get_location(loc_id)
    if not loc or loc.user != session['username']:
        return jsonify({'error': 'Location not found'}), 404
    return jsonify({'id': loc.loc_id, 'name': loc.name, 'lat': loc.lat, 'lng': loc.lng, 'description': loc.description})

@favorite_locations_bp.route('/locations/<int:loc_id>', methods=['PUT'])
def update_location(loc_id):
    auth = require_login()
    if auth:
        return auth
    loc = favorite_locations_model.get_location(loc_id)
    if not loc or loc.user != session['username']:
        return jsonify({'error': 'Location not found'}), 404
    data = request.get_json()
    updated = favorite_locations_model.update_location(loc_id, **data)
    return jsonify({'id': updated.loc_id, 'name': updated.name, 'lat': updated.lat, 'lng': updated.lng, 'description': updated.description})

@favorite_locations_bp.route('/locations/<int:loc_id>', methods=['DELETE'])
def delete_location(loc_id):
    auth = require_login()
    if auth:
        return auth
    loc = favorite_locations_model.get_location(loc_id)
    if not loc or loc.user != session['username']:
        return jsonify({'error': 'Location not found'}), 404
    favorite_locations_model.delete_location(loc_id)
    return jsonify({'message': 'Location deleted'})