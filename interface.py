import os
from flask import Flask, render_template, request, jsonify
import project_app.config as config
from project_app.utils import ThroughputPrediction

app = Flask(__name__)

############################################################################################################
######################################### Home API ########################################################
############################################################################################################


@app.route('/')
def home():
    print('Welcome to the Throughput Prediction Homepage')
    return render_template('home.html')

############################################################################################################
######################################### Model API ########################################################
############################################################################################################


@app.route('/predict_throughput', methods=['GET', 'POST'])
def predict_throughput():
    if request.method == 'POST':
        print('We are using POST method')
        data = request.get_json()  # json while sending data from postman
        print('Data:', data) 
        band = data['band']
        ran = data['ran']
        rsrq = float(data['rsrq'])
        rssi = float(data['rssi'])
        rsrp = float(data['rsrp'])
        sinr = float(data['sinr'])
        delay = float(data['delay'])
        throughput_uplink = float(data['throughput_uplink'])
        velocity_abs = float(data['velocity_abs'])
        acceleration_abs = float(data['acceleration_abs'])
        acceleration_long = float(data['acceleration_long'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        throughput_prediction = ThroughputPrediction(band, ran, rsrq, rssi, rsrp, sinr, delay,
                                                     throughput_uplink, velocity_abs,
                                                     acceleration_abs, acceleration_long,
                                                     latitude, longitude)
        predicted_throughput = throughput_prediction.get_predicted_throughput()
        return jsonify({'Result': f'Predicted Throughput for the given input data is: {round(predicted_throughput, 2)} Kbps'})

    else:
        print('We are using GET method')
        data = request.args   # query parameters
        print('Data:', data)
        band = data['band']
        ran = data['ran']
        rsrq = float(data['rsrq'])
        rssi = float(data['rssi'])
        rsrp = float(data['rsrp'])
        sinr = float(data['sinr'])
        delay = float(data['delay'])
        throughput_uplink = float(data['throughput_uplink'])
        velocity_abs = float(data['velocity_abs'])
        acceleration_abs = float(data['acceleration_abs'])
        acceleration_long = float(data['acceleration_long'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        throughput_prediction = ThroughputPrediction(band, ran, rsrq, rssi, rsrp, sinr, delay,  throughput_uplink=throughput_uplink, velocity_abs=velocity_abs, acceleration_abs=acceleration_abs, acceleration_long=acceleration_long, latitude=latitude, longitude=longitude)
        predicted_throughput = throughput_prediction.get_predicted_throughput()
        return jsonify({'Result': f'Predicted Throughput for the given input data is: {round(predicted_throughput, 2)} Kbps'})      

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5004)))
