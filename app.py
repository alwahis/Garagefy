from flask import Flask, render_template, request, jsonify
from car_diagnostic import CarDiagnosticSystem
from car_database import car_database
from data import CAR_BRANDS
from luxembourg_garages import LUXEMBOURG_GARAGES

app = Flask(__name__)
diagnostic_system = CarDiagnosticSystem()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnose')
def diagnose_page():
    return render_template('diagnose.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose_car():
    data = request.json
    try:
        result = diagnostic_system.diagnose_issue(
            symptoms=data['symptoms'],
            car_brand=data['car_brand'],
            car_model=data['car_model'],
            year=data['year']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/brands')
def get_brands():
    return jsonify(list(CAR_BRANDS.keys()))

@app.route('/api/models/<brand>')
def get_models(brand):
    if brand in CAR_BRANDS:
        return jsonify(list(CAR_BRANDS[brand]["models"].keys()))
    return jsonify([])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
