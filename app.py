from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import logging
import random
from datetime import datetime, timedelta
import requests
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app with explicit template and static folders
app = Flask(__name__, template_folder='templates', static_folder='static')
# Restrict CORS to your app's URL in production
CORS(app, resources={r"/api/*": {"origins": ["https://solarforecastapp.onrender.com", "http://localhost:5000"]}})

def generate_forecast_data():
    now = datetime.now()
    forecast = []
    for i in range(24):  # 24-hour forecast
        date_time = (now + timedelta(hours=i)).strftime('%Y-%m-%dT%H:00:00')
        predicted = random.uniform(400, 600)  # Simulated predicted power in kW
        actual = predicted * random.uniform(0.9, 1.1)  # Simulated actual power
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
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key:
            logging.error("OPENWEATHERMAP_API_KEY not set")
            return jsonify({"error": "Weather API key not configured", "list": [{"weather": [{"description": "Weather data unavailable"}]}]}), 500
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat=28.6139&lon=77.2090&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info("Weather data fetched successfully from OpenWeatherMap")
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        return jsonify({"error": f"Failed to fetch weather data: {str(e)}", "list": [{"weather": [{"description": "Weather data unavailable"}]}]}), 500

@app.route('/')
def home():
    try:
        logging.info("Attempting to render index.html")
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error rendering index.html: {str(e)}", exc_info=True)
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        logging.error(f"Error serving favicon.ico: {str(e)}", exc_info=True)
        return jsonify({"error": "Favicon not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(debug=False, host='0.0.0.0', port=port)
