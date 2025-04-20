from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import random
from datetime import datetime, timedelta
import requests

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api/* routes

def generate_forecast_data():
    now = datetime.now()
    forecast = []
    for i in range(24):  # 24-hour forecast
        date_time = (now + timedelta(hours=i)).strftime('%Y-%m-%dT%H:00:00')
        predicted = random.uniform(400, 600)  # Simulated predicted power in kW
        actual = predicted * random.uniform(0.9, 1.1)  # Simulated actual power with slight variation
        forecast.append({"date_time": date_time, "predicted": round(predicted, 2), "actual": round(actual, 2)})
    metrics = {
        "mae": random.uniform(5, 15),    # Mean Absolute Error
        "rmse": random.uniform(10, 20),  # Root Mean Squared Error
        "mape": random.uniform(1, 5),    # Mean Absolute Percentage Error
        "r2": random.uniform(0.9, 0.99)  # R-squared
    }
    return {"forecast": forecast, "metrics": metrics}

def generate_historical_data():
    now = datetime.now()
    historical = []
    for i in range(1, 25):  # Last 24 hours
        date_time = (now - timedelta(hours=i)).strftime('%Y-%m-%dT%H:00:00')
        actual = random.uniform(400, 600)  # Simulated historical power in kW
        historical.append({"date_time": date_time, "actual": round(actual, 2)})
    return historical

@app.route('/api/forecast')
def forecast():
    try:
        date_range = request.args.get('date_range', 'all')
        power_type = request.args.get('power_type', 'AC')
        inverter = request.args.get('inverter', 'all')
        logging.info(f"Received forecast request: date_range={date_range}, power_type={power_type}, inverter={inverter}")
        data = generate_forecast_data()
        logging.info("Forecast data generated successfully")
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error in forecast endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/historical')
def historical():
    try:
        date_range = request.args.get('date_range', 'all')
        logging.info(f"Received historical request: date_range={date_range}")
        data = generate_historical_data()
        logging.info("Historical data generated successfully")
        return jsonify(data)
    except Exception as e:
        logging.error(f"Error in historical endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/map')
def get_map_data():
    try:
        api_key = "bd47081533c66550286112892cea28c4"
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat=28.6139&lon=77.2090&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        logging.info("Weather data fetched successfully from OpenWeatherMap")
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}", "list": [{"weather": [{"description": "Weather data unavailable"}]}]}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')