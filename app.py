from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_TOKEN = "d0df25a59e5a163cee4520c8c6d62f160373c421"

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "#2ecc71"
    elif aqi <= 100:
        return "Moderate", "#f39c12"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "#e67e22"
    elif aqi <= 200:
        return "Unhealthy", "#e74c3c"
    else:
        return "Hazardous", "#8e44ad"

def get_health_tip(aqi):
    if aqi <= 50:
        return "Air quality is good. Enjoy outdoor activities freely."
    elif aqi <= 100:
        return "Air quality is acceptable. Sensitive people should reduce prolonged outdoor activities."
    elif aqi <= 150:
        return "Sensitive groups should reduce outdoor activities. Wear a mask if going outside."
    elif aqi <= 200:
        return "Everyone should reduce outdoor activities. Wear a mask outside. Keep windows closed."
    else:
        return "Health alert. Avoid all outdoor activities. Stay indoors. Use air purifier if available."

def fetch_aqi(url):
    response = requests.get(url, timeout=5)
    data = response.json()
    if data["status"] != "ok":
        return None
    iaqi = data["data"]["iaqi"]
    aqi = data["data"]["aqi"]
    category, color = get_aqi_category(aqi)
    health_tip = get_health_tip(aqi)
    return {
        "city": data["data"]["city"]["name"],
        "aqi": aqi,
        "category": category,
        "color": color,
        "health_tip": health_tip,
        "pm25": iaqi.get("pm25", {}).get("v", "N/A"),
        "pm10": iaqi.get("pm10", {}).get("v", "N/A"),
        "no2":  iaqi.get("no2",  {}).get("v", "N/A"),
        "so2":  iaqi.get("so2",  {}).get("v", "N/A"),
        "co":   iaqi.get("co",   {}).get("v", "N/A"),
    }

@app.route('/city', methods=['GET'])
def city_aqi():
    try:
        city = request.args.get('city')
        url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"
        data = fetch_aqi(url)
        if data:
            return jsonify({"status": "ok", "data": data})
        return jsonify({"status": "error", "message": "City not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        lat = float(request.args.get('lat', 0))
        lon = float(request.args.get('lon', 0))

        url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_TOKEN}"
        data = fetch_aqi(url)

        if not data:
            search_url = f"https://api.waqi.info/map/bounds/?latlng={lat-1},{lon-1},{lat+1},{lon+1}&token={API_TOKEN}"
            search_response = requests.get(search_url, timeout=5)
            search_data = search_response.json()
            if search_data["status"] == "ok" and len(search_data["data"]) > 0:
                nearest = search_data["data"][0]
                station_url = f"https://api.waqi.info/feed/@{nearest['uid']}/?token={API_TOKEN}"
                data = fetch_aqi(station_url)

        if data:
            return jsonify({"status": "ok", "data": data})
        return jsonify({"status": "error", "message": "No AQI station found near you"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)