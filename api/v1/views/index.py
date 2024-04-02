#!/usr/bin/python3
'''
Creates Flask app,
'''

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """
    Returns the status of the API.
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_stats():
    """
    Returns the stats of the API.
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'users': storage.count('Users'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'cities': storage.count('City'),
    }

    return jsonify(stats)