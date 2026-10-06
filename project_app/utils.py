import pickle
import json
import numpy as np
from project_app import config

class ThroughputPrediction():

    def __init__(self, band, ran, rsrq, rssi, rsrp, sinr, delay, throughput_uplink,
                 velocity_abs, acceleration_abs, acceleration_long,
                 latitude, longitude):
        self.band = band
        self.ran = ran
        self.rsrq = rsrq
        self.rssi = rssi
        self.rsrp = rsrp
        self.sinr = sinr
        self.delay = delay
        self.throughput_uplink = throughput_uplink
        self.velocity_abs = velocity_abs
        self.acceleration_abs = acceleration_abs
        self.acceleration_long = acceleration_long
        self.latitude = latitude
        self.longitude = longitude

        
    def load_model(self):
        with open(config.MODEL_FILE_PATH, 'rb') as f:
            self.model = pickle.load(f)

        with open(config.JSON_FILE_PATH, 'r') as f:
            self.project_data = json.load(f)

        with open(config.SCALER_FILE_PATH, 'rb') as f:
            self.scaler = pickle.load(f)

        with open(config.TRANSFORMER_MODEL_PATH, 'rb') as f:
            self.transformer = pickle.load(f)


    def get_predicted_throughput(self):
        self.load_model()
        test_array = np.zeros(self.model.n_features_in_)  

        self.ran = 'ran_' + self.ran
        self.band = 'band_' + self.band
        ran_idx = self.project_data['columns'].index(self.ran)
        band_idx = self.project_data['columns'].index(self.band)

        test_array[band_idx] = 1
        test_array[ran_idx] = 1
        test_array[7] = self.rsrq
        test_array[8] = self.rssi
        test_array[9] = self.rsrp
        test_array[10] = self.sinr
        test_array[11] = self.delay
        test_array[12] = self.throughput_uplink
        test_array[13] = self.velocity_abs
        test_array[14] = self.acceleration_abs
        test_array[15] = self.acceleration_long
        test_array[16] = self.latitude
        test_array[17] = self.longitude

        print("Test Array:", test_array)  

        # Apply Yeo-Johnson transformation to the numerical features
        transform_data = [[
            self.acceleration_abs,
            self.rsrq,
            self.rssi,
            self.rsrp,
            self.acceleration_long,
            self.delay,
            self.throughput_uplink
        ]]

        transform_data = self.transformer.transform(transform_data)[0]

        for col, value in zip(self.project_data['transformer'], transform_data):
            idx = self.project_data['columns'].index(col)
            test_array[idx] = value

        # Scale the features using the loaded scaler
        scaled_test_array = self.scaler.transform([test_array[7:]])[0]

        final_test_array = np.concatenate((test_array[:7], scaled_test_array), axis=0)

        predicted_throughput = self.model.predict([final_test_array])[0]
        print(f'Predicted throughput for the given input data is: {round(predicted_throughput, 2)} Kbps')

        return predicted_throughput


if __name__ == "__main__":
    band = 'LTE_B1'
    ran = 'LTE'
    rsrq = -10.0
    rssi = -70.0
    rsrp = -90.0
    sinr = 20.0
    delay = 50.0
    throughput_uplink = 10.0
    velocity_abs = 30.0
    acceleration_abs = 2.0
    acceleration_long = 1.0
    latitude = 37.7749
    longitude = -122.4194

    throughput_prediction = ThroughputPrediction(band, ran, rsrq, rssi, rsrp, sinr, delay,
                                                 throughput_uplink, velocity_abs,
                                                 acceleration_abs, acceleration_long,
                                                 latitude, longitude)
    predicted_throughput = throughput_prediction.get_predicted_throughput()
    print("Predicted Throughput:", predicted_throughput)