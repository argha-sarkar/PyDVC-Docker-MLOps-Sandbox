import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Check if the model is available locally, if not, pull it from DVC
if not os.path.exists('models/model.joblib'):
    print("Model not found. Running dvc pull...")
    # This command requires DVC to be installed and configured in the container.
    # For a full CI/CD pipeline, this step would be handled by the runner.
    # For this demonstration, we assume the model is available or pulled on start.
    # A more robust approach is to have the CI/CD pipeline provision the model
    # or have the container pull from the remote storage on startup.
    os.system('dvc pull models/model.joblib')

# Load the trained model on startup
try:
    model = joblib.load('models/model.joblib')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file not found. Ensure dvc pull was successful.")
    model = None

@app.route('/')
def home():
    return "ML Model Inference Service is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        json_ = request.json
        # Assume input is a list of features, e.g., [[5.1, 3.5, 1.4, 0.2]]
        df = pd.DataFrame(json_)
        prediction = model.predict(df).tolist()
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
