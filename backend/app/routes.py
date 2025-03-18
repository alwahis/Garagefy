from flask import Blueprint, jsonify, request
import logging
from .services.ai_service import CarDiagnosticAI
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__)

# Initialize AI service
car_diagnostic_ai = CarDiagnosticAI()

@api.route('/car-data', methods=['GET'])
def get_car_data():
    """Get available car brands and models"""
    try:
        car_data = {
            'Toyota': {
                'models': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Prius', 'Land Cruiser', 'Tundra', 'Tacoma', 'Sienna', '4Runner']
            },
            'Honda': {
                'models': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V', 'Odyssey', 'Ridgeline', 'Fit', 'Passport', 'Insight']
            },
            'Ford': {
                'models': ['F-150', 'Mustang', 'Explorer', 'Escape', 'Focus', 'Bronco', 'Ranger', 'Edge', 'Expedition', 'Maverick']
            },
            'BMW': {
                'models': ['3 Series', '5 Series', 'X3', 'X5', 'M3', '7 Series', 'X1', 'X7', 'i4', 'iX']
            },
            'Mercedes-Benz': {
                'models': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'A-Class', 'GLA', 'GLB', 'EQS', 'G-Class']
            },
            'Audi': {
                'models': ['A4', 'A6', 'Q5', 'Q7', 'TT', 'A3', 'Q3', 'e-tron', 'RS6', 'S5']
            },
            'Nissan': {
                'models': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Maxima', 'Frontier', 'Kicks', 'Murano', 'Armada', 'Leaf']
            },
            'Hyundai': {
                'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona', 'Palisade', 'Venue', 'IONIQ', 'Accent', 'Genesis']
            },
            'Chevrolet': {
                'models': ['Silverado', 'Equinox', 'Malibu', 'Tahoe', 'Camaro', 'Traverse', 'Blazer', 'Colorado', 'Suburban', 'Bolt']
            },
            'Kia': {
                'models': ['Soul', 'Sportage', 'Sorento', 'Optima', 'Forte', 'Telluride', 'Seltos', 'Carnival', 'Niro', 'EV6']
            },
            'Volkswagen': {
                'models': ['Golf', 'Passat', 'Tiguan', 'Atlas', 'Jetta', 'ID.4', 'Taos', 'Arteon', 'GTI', 'R']
            },
            'Lexus': {
                'models': ['RX', 'ES', 'NX', 'IS', 'GX', 'UX', 'LS', 'LC', 'RC', 'LX']
            },
            'Porsche': {
                'models': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan', '718 Cayman', '718 Boxster', 'Cayenne Coupe']
            },
            'Subaru': {
                'models': ['Outback', 'Forester', 'Crosstrek', 'Impreza', 'Legacy', 'Ascent', 'WRX', 'BRZ', 'Solterra']
            },
            'Mazda': {
                'models': ['CX-5', 'Mazda3', 'CX-30', 'CX-9', 'MX-5 Miata', 'CX-50', 'Mazda6', 'MX-30']
            },
            'Volvo': {
                'models': ['XC90', 'XC60', 'S60', 'V60', 'XC40', 'S90', 'V90', 'C40', 'Polestar 2']
            },
            'Land Rover': {
                'models': ['Range Rover', 'Discovery', 'Defender', 'Range Rover Sport', 'Range Rover Velar', 'Discovery Sport', 'Evoque']
            },
            'Jeep': {
                'models': ['Grand Cherokee', 'Wrangler', 'Cherokee', 'Compass', 'Renegade', 'Gladiator', 'Wagoneer', 'Grand Wagoneer']
            },
            'Acura': {
                'models': ['MDX', 'RDX', 'TLX', 'ILX', 'NSX', 'Integra']
            },
            'Infiniti': {
                'models': ['Q50', 'QX60', 'QX80', 'QX50', 'Q60', 'QX55']
            }
        }
        return jsonify(car_data)
    except Exception as e:
        logger.error(f"Error fetching car data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/diagnose', methods=['POST'])
async def diagnose_car():
    """Diagnose car issues using technical documentation and AI"""
    try:
        data = request.get_json()
        brand = data.get('brand')
        model = data.get('model')
        year = data.get('year')
        symptoms = data.get('symptoms')

        # Validate required fields
        if not all([brand, model, year, symptoms]):
            return jsonify({
                'error': 'Missing required fields. Please provide brand, model, year, and symptoms.'
            }), 400

        # Format the problem description
        problem_description = f"Vehicle: {year} {brand} {model}\nSymptoms: {symptoms}"
        
        try:
            # Get AI-powered diagnosis with technical documentation
            diagnosis = await car_diagnostic_ai.get_diagnosis(brand, problem_description)
            
            response = {
                'diagnosis': {
                    'vehicle_info': {
                        'brand': brand,
                        'model': model,
                        'year': year
                    },
                    'symptoms': symptoms,
                    'analysis': diagnosis,
                    'disclaimer': (
                        'This diagnosis is provided by an AI system with access to technical documentation. '
                        'Always consult with a qualified mechanic for a professional inspection.'
                    )
                }
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error with AI diagnosis: {str(e)}")
            return jsonify({
                'error': 'An error occurred during diagnosis. Please try again.'
            }), 500

    except Exception as e:
        logger.error(f"Error in diagnosis endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/test', methods=['GET'])
async def test_connection():
    """Test the diagnostic system"""
    try:
        # Test diagnosis for a common issue
        test_brand = "Toyota"
        test_symptoms = "Engine makes knocking sound and check engine light is on"
        
        diagnosis = await car_diagnostic_ai.get_diagnosis(test_brand, test_symptoms)
        
        return jsonify({
            'status': 'success',
            'message': 'Diagnostic system is working',
            'test_diagnosis': diagnosis
        })
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/garages', methods=['GET'])
def get_garages():
    """Get garages near the user's location"""
    try:
        # Get latitude and longitude from request parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        
        # Check if we have the required location data
        if not lat or not lng:
            return jsonify({
                'error': 'Missing location data. Please provide lat and lng parameters.'
            }), 400
            
        # For now, return sample garage data
        sample_garages = [
            {
                "id": 1,
                "name": "Burger King Auto Center",
                "address": "123 Main St, Anytown, USA",
                "phone": "555-123-4567",
                "website": "https://www.burgerkingauto.com",
                "rating": 4.8,
                "reviews": 128,
                "hours": "Mon-Fri: 8AM-6PM, Sat: 9AM-5PM, Sun: Closed",
                "distance": 1.2,
                "services": "Oil Change, Tire Rotation, Brake Service, Engine Repair, Transmission Service",
                "url": "https://www.burgerkingauto.com"
            },
            {
                "id": 2,
                "name": "BK Car Care Center",
                "address": "456 Oak Ave, Somewhere, USA",
                "phone": "555-987-6543",
                "website": "https://www.bkcarcare.com",
                "rating": 4.6,
                "reviews": 94,
                "hours": "Mon-Sat: 7AM-7PM, Sun: 10AM-4PM",
                "distance": 2.5,
                "services": "Oil Change, Brake Service, Wheel Alignment, Electrical System, A/C Service",
                "url": "https://www.bkcarcare.com"
            },
            {
                "id": 3,
                "name": "Flame Grilled Auto Shop",
                "address": "789 Pine Rd, Nowhere, USA",
                "phone": "555-456-7890",
                "website": "https://www.flamegrillautoshop.com",
                "rating": 4.9,
                "reviews": 216,
                "hours": "Mon-Fri: 7:30AM-6:30PM, Sat-Sun: 8AM-5PM",
                "distance": 3.7,
                "services": "Diagnostics, Complete Engine Repair, Transmission Repair, Wheel Balancing, Oil Change",
                "url": "https://www.flamegrillautoshop.com"
            },
            {
                "id": 4,
                "name": "Whopper Automotive",
                "address": "321 Elm St, Anywhere, USA",
                "phone": "555-789-0123",
                "website": "https://www.whopperautomotive.com",
                "rating": 4.7,
                "reviews": 163,
                "hours": "Mon-Fri: 8AM-7PM, Sat: 8AM-5PM, Sun: Closed",
                "distance": 4.2,
                "services": "Full Service Auto Repair, Brake Service, Electrical Repair, Performance Upgrades, Muffler & Exhaust",
                "url": "https://www.whopperautomotive.com"
            },
            {
                "id": 5,
                "name": "The King's Garage",
                "address": "654 Walnut Blvd, Somewhere, USA",
                "phone": "555-321-6547",
                "website": "https://www.kingsgarage.com",
                "rating": 4.5,
                "reviews": 87,
                "hours": "Mon-Thu: 8AM-6PM, Fri: 8AM-5PM, Sat-Sun: Closed",
                "distance": 5.8,
                "services": "Tune-ups, Wheel Alignment, Battery Service, Check Engine Light, Preventive Maintenance",
                "url": "https://www.kingsgarage.com"
            }
        ]
        
        return jsonify({
            'garages': sample_garages
        })
        
    except Exception as e:
        logger.error(f"Error fetching garages: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch garages. Please try again later.'
        }), 500
