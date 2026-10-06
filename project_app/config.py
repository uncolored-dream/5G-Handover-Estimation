import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_FILE_PATH = os.path.join(BASE_DIR, "dt_model.pkl")
JSON_FILE_PATH = os.path.join(BASE_DIR, "project_data.json")
SCALER_FILE_PATH = os.path.join(BASE_DIR, "scaler.pkl")
TRANSFORMER_MODEL_PATH = os.path.join(BASE_DIR, "yeo_transformer_model.pkl")

HOST = "0.0.0.0"
PORT = 5004