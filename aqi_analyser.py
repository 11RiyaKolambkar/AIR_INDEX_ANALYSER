import requests
import numpy as np
import pandas as pd

API_TOKEN = "d0df25a59e5a163cee4520c8c6d62f160373c421"  # paste your WAQI token here

# STEP 1: Auto-detect your city from IP
def get_my_city():
    response = requests.get("https://ipapi.co/json/")
    data = response.json()
    city = data["city"]
    print(f"Detected Location: {city}, {data['country_name']}")
    return city

# STEP 2: Fetch real-time AQI for that city
def get_realtime_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        raise ValueError(f"API error: {data['data']}")

    iaqi = data["data"]["iaqi"]

    record = {
        "City":  data["data"]["city"]["name"],
        "AQI":   data["data"]["aqi"],
        "PM2.5": iaqi.get("pm25", {}).get("v", np.nan),
        "PM10":  iaqi.get("pm10", {}).get("v", np.nan),
        "NO2":   iaqi.get("no2",  {}).get("v", np.nan),
        "SO2":   iaqi.get("so2",  {}).get("v", np.nan),
        "CO":    iaqi.get("co",   {}).get("v", np.nan),
        "O3":    iaqi.get("o3",   {}).get("v", np.nan),
    }
    return pd.DataFrame([record])

# STEP 3: Predict AQI category
def predict_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# MAIN
city = get_my_city()
df = get_realtime_aqi(city)

# Clean missing values
for col in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]:
    df[col] = df[col].fillna(df[col].mean())

# Predict
aqi_value = df["AQI"].values[0]
category = predict_category(aqi_value)

print(f"\nCity     : {df['City'].values[0]}")
print(f"AQI      : {aqi_value}")
print(f"Category : {category}")
print(f"\nPollutants:")
print(df[["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]].to_string(index=False))