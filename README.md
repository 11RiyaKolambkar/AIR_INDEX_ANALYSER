# Air Quality Index Analyser

A real-time Air Quality Index (AQI) prediction web application built using Python, Flask, and Machine Learning. The app automatically detects your location using GPS and fetches live pollution data from the nearest monitoring station.

## Features
- Real-time AQI data using WAQI API
- Auto location detection using browser GPS
- Machine Learning model to predict AQI
- Color coded AQI category display
- Manual input option for custom values

## Technologies Used
- Python
- Flask
- Scikit-learn
- Pandas, NumPy
- WAQI Real-time API
- HTML, CSS
- JavaScript

## How to Run

1. Clone the repository
   git clone https://github.com/11RiyaKolambkar/AIR_INDEX_ANALYSER.git

2. Install dependencies
   pip install flask scikit-learn pandas numpy requests joblib

3. Add your WAQI API token in app.py
   API_TOKEN = "your_token_here"

4. Run the app
   python app.py

5. Open in browser
   http://localhost:5000

## How it Works
1. User clicks "Detect My Location"
2. Browser GPS detects coordinates
3. App fetches real-time pollutant data from nearest AQI station
4. Machine Learning model predicts AQI value
5. Result is displayed with category and color

## AQI Categories
- 0-50: Good
- 51-100: Moderate
- 101-150: Unhealthy for Sensitive Groups
- 151-200: Unhealthy
- 200+: Hazardous

## Dataset
Model trained on India city-wise daily AQI dataset containing PM2.5, PM10, NO2, SO2, CO values.

## Author
Riya Kolambkar
MCA Student
