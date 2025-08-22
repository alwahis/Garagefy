from flask import Blueprint, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask Blueprint
api = Blueprint('api', __name__)

@api.route('/car-data', methods=['GET'])
def get_car_data():
    """Get available car brands and models"""
    try:
        return jsonify({
            'Toyota': {'models': ['Camry', 'Corolla', 'RAV4']},
            'Honda': {'models': ['Civic', 'Accord', 'CR-V']},
            'Ford': {'models': ['F-150', 'Mustang', 'Explorer']}
        })
    except Exception as e:
        logger.error(f"Error fetching car data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/garages/nearby', methods=['GET'])
def get_nearby_garages():
    """Get nearby garages with static test data"""
    try:
        return jsonify([
            {"id": 1, "name": "Test Garage", "services": ["oil change"]},
            {"id": 2, "name": "Quick Fix", "services": ["tire repair"]}
        ])
    except Exception as e:
        logger.error(f"Error fetching garages: {str(e)}")
        return jsonify({'error': 'Failed to fetch garages'}), 500


