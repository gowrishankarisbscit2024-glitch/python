import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap.
# You can get one for free by signing up at: https://home.openweathermap.org/users/sign_up
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'YOUR_API_KEY')
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def index():
    """Serves the main HTML page for the weather app."""
    return render_template('weather.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Fetches weather data for a given city from the OpenWeatherMap API.

    The city name is passed as a query parameter 'city'.
    Returns a JSON object with weather details or an error message.
    """
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    # The parameters for the API request
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        weather_data = response.json()

        if 'main' not in weather_data:
            return jsonify({'error': 'City not found or invalid response'}), 404

        # Extract the relevant weather information
        weather_info = {
            'city': weather_data['name'],
            'country': weather_data['sys']['country'],
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'].capitalize(),
            'icon_url': f"https://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png",
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }
        return jsonify(weather_info)

    except requests.exceptions.RequestException as e:
        # Handle network or API-related errors
        return jsonify({'error': f'An error occurred: {e}'}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    # You can set the host to '0.0.0.0' to make it accessible from other devices on your network
    app.run(debug=True, host='127.0.0.1', port=5000)
