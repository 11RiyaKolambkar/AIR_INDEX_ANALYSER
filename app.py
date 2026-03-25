from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('aqi_model.pkl')

def get_aqi_category(aqi):
    if aqi <= 50:
        category= "Good"
        color="#2ecc71"
    elif aqi <= 100:
        category="Moderate"
        color="#f39c12"
    elif aqi <= 150:
       category= "Unhealthy for Sensitive Groups"
       color="#e67e22"
    elif aqi <= 200:
        category="Unhealthy"
        color="#e74c3c"
    else:
        category= "Hazardous",
        color="#8e44ad"
        return category, color

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
        category, color,  = get_aqi_category(prediction)

    return render_template('index.html',
                         prediction=prediction,
                         category=category,
                         color=color,
                        )

if __name__ == '__main__':
    app.run(debug=True)