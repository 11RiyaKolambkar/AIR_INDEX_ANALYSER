from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import requests

app = Flask(__name__)
model = joblib.load('aqi_model.pkl')

API_TOKEN = "d0df25a59e5a163cee4520c8c6d62f160373c421"  # paste your WAQI token here

def get_aqi_category(aqi):
    if aqi <= 50:
        category = "Good"
        color = "#2ecc71"
    elif aqi <= 100:
        category = "Moderate"
        color = "#f39c12"
    elif aqi <= 150:
        category = "Unhealthy for Sensitive Groups"
        color = "#e67e22"
    elif aqi <= 200:
        category = "Unhealthy"
        color = "#e74c3c"
    else:
        category = "Hazardous"
        color = "#8e44ad"
    return category, color  # this was missing in your original code

def get_my_location():
    response = requests.get("https://ipapi.co/json/", timeout=5)
    data = response.json()
    lat = data.get("latitude")
    lon = data.get("longitude")
    print(f"Detected coordinates: {lat}, {lon}")
    return lat, lon

def get_realtime_aqi_by_coords(lat, lon):
    lat = float(lat)
    lon = float(lon)

    # First try exact coordinates
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_TOKEN}"
    response = requests.get(url, timeout=5)
    data = response.json()

    if data["status"] == "ok":
        iaqi = data["data"]["iaqi"]
        return {
            "city":  data["data"]["city"]["name"],
            "aqi":   data["data"]["aqi"],
            "pm25":  iaqi.get("pm25", {}).get("v", 0),
            "pm10":  iaqi.get("pm10", {}).get("v", 0),
            "no2":   iaqi.get("no2",  {}).get("v", 0),
            "so2":   iaqi.get("so2",  {}).get("v", 0),
            "co":    iaqi.get("co",   {}).get("v", 0),
        }

    # Search nearby stations
    search_url = f"https://api.waqi.info/map/bounds/?latlng={lat-1},{lon-1},{lat+1},{lon+1}&token={API_TOKEN}"
    search_response = requests.get(search_url, timeout=5)
    search_data = search_response.json()

    if search_data["status"] == "ok" and len(search_data["data"]) > 0:
        nearest = search_data["data"][0]
        station_url = f"https://api.waqi.info/feed/@{nearest['uid']}/?token={API_TOKEN}"
        station_response = requests.get(station_url, timeout=5)
        station_data = station_response.json()

        if station_data["status"] == "ok":
            iaqi = station_data["data"]["iaqi"]
            return {
                "city":  station_data["data"]["city"]["name"],
                "aqi":   station_data["data"]["aqi"],
                "pm25":  iaqi.get("pm25", {}).get("v", 0),
                "pm10":  iaqi.get("pm10", {}).get("v", 0),
                "no2":   iaqi.get("no2",  {}).get("v", 0),
                "so2":   iaqi.get("so2",  {}).get("v", 0),
                "co":    iaqi.get("co",   {}).get("v", 0),
            }

    return None
@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            # fallback to IP
            response = requests.get("https://ipapi.co/json/", timeout=5)
            data = response.json()
            lat = data.get("latitude")
            lon = data.get("longitude")

        data = get_realtime_aqi_by_coords(lat, lon)

        if data:
            return jsonify({"status": "ok", "data": data})
        else:
            return jsonify({"status": "error", "message": "No AQI station found near you"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/', methods=['GET', 'POST'])
def predict():
    prediction = None
    category = None
    color = None

    if request.method == 'POST':
        pm25 = float(request.form['pm25'])
        pm10 = float(request.form['pm10'])
        no2 = float(request.form['no2'])
        co = float(request.form['co'])
        so2 = float(request.form['so2'])

        input_data = np.array([[pm25, pm10, no2, co, so2]])
        prediction = round(model.predict(input_data)[0], 2)
        category, color = get_aqi_category(prediction)

    return render_template('index.html',
                           prediction=prediction,
                           category=category,
                           color=color)

if __name__ == '__main__':
    app.run(debug=True)