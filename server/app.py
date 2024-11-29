# FILE: server/app.py
# This server handles three endpoints:
# 1. Root endpoint that provides a welcome message.
# 2. Accepts the day of the week and airport ID, calls the model, and returns the prediction and confidence.
# 3. Returns the list of airport names and IDs, sorted alphabetically.

from flask import Flask, request, jsonify
import pandas as pd
import joblib
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import data

app = Flask(__name__)

# Load the model
model = joblib.load('/workspaces/hackathon-team-4/data/flight_delay_model.pkl')

@app.route('/')
def index():
    return "Welcome to the Flight Delay Prediction API. Use /predict to get predictions and /airports to get the list of airports."

@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    day_of_week = content['day_of_week']
    origin_airport_id = content['origin_airport_id']
    dest_airport_id = content['dest_airport_id']
    carrier = content['carrier']

    # Create a DataFrame for the input with all required columns
    input_data = pd.DataFrame({
        'Year': [2024],  # Default value
        'Month': [1],  # Default value
        'DayofMonth': [1],  # Default value
        'DayOfWeek': [day_of_week],
        'CRSDepTime': [0],  # Default value
        'DepDelay': [0],  # Default value
        'DepDel15': [0],  # Default value
        'CRSArrTime': [0],  # Default value
        'ArrDel15': [0],  # Default value
        'Cancelled': [0],  # Default value
        'OriginAirportID': [origin_airport_id],
        'DestAirportID': [dest_airport_id],
        'Carrier': [carrier]
    })

    # Preprocess the input data
    # Assuming the preprocessing steps are defined in the model pipeline
    prediction = model.predict(input_data)
    confidence = model.predict_proba(input_data).max()

    return jsonify({
        'prediction': int(prediction[0]),
        'confidence': float(confidence)
    })

@app.route('/airports', methods=['GET'])
def airports():
    airports = data[['OriginAirportID', 'OriginAirportName']].drop_duplicates().sort_values(by='OriginAirportName')
    airports_list = airports.to_dict(orient='records')
    return jsonify(airports_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)