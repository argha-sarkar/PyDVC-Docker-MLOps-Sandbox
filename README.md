MLOps Local Project
This project serves as a hands-on, reproducible MLOps pipeline using key open-source tools. The goal is to demonstrate a complete machine learning workflow, from data versioning to containerized deployment, all on your local machine.

Key Features
Python: The core language for data processing and model training.

Git: Used for source code version control.

DVC (Data Version Control): Manages and versions large datasets and models, keeping them separate from the Git repository.

Docker: Containers the entire application for consistent, reproducible execution.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.8+

Git

Docker

DVC (Data Version Control)

Project Structure
The project is organized into a clean and logical structure:

mlops-local-project/
├── data/              # Stores the DVC-tracked dataset
├── models/            # Stores the trained model
├── src/
│   ├── __init__.py    # Makes the directory a Python package
│   ├── prepare_data.py  # Script to generate/prepare data
│   ├── train.py       # Script to train the ML model
├── .gitignore         # Defines files to ignore in Git
├── app.py             # Flask API for model inference
├── DVC.yaml           # DVC pipeline definition
└── requirements.txt   # Python dependencies

Getting Started
Follow these steps to set up and run the project locally.

Step 1: Project Setup
Initialize Git:

mkdir mlops-local-project
cd mlops-local-project
git init

Create Directories & Files:
Create the folder structure as shown above.

Setup Python Environment:

python -m venv venv
source venv/bin/activate

Install Dependencies:
Add the following to requirements.txt:

scikit-learn
pandas
joblib
flask
gunicorn
dvc

Then, install them:

pip install -r requirements.txt

Configure .gitignore:
Add the following content to your .gitignore file:

venv/
__pycache__/
*.pyc
data/
models/
.env
.dvc/

Step 2: Data Versioning with DVC
Initialize DVC:

dvc init

Create and Track Data:
Write a simple data preparation script in src/prepare_data.py.

import pandas as pd
from sklearn.datasets import load_iris
import os

def prepare_data():
    """Loads the iris dataset and saves it to a CSV."""
    print("Preparing data...")
    os.makedirs('data', exist_ok=True)
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df.to_csv('data/iris.csv', index=False)
    print("Data preparation complete.")

if __name__ == "__main__":
    prepare_data()

Then, run the script and track the data with DVC and Git:

python src/prepare_data.py
dvc add data/iris.csv
git add data/iris.csv.dvc
git commit -m "Add iris dataset with DVC"

Step 3: Model Training and DVC Pipeline
Create the Training Script:
Write the training logic in src/train.py.

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_model():
    """Trains a RandomForestClassifier and saves the model."""
    print("Starting model training...")
    df = pd.read_csv('data/iris.csv')
    X = df.drop('target', axis=1)
    y = df['target']

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.joblib')
    print("Model training complete. Model saved to models/model.joblib")

if __name__ == "__main__":
    train_model()

Define the DVC Pipeline:
Create a DVC.yaml file to define the pipeline stages.

stages:
  prepare:
    cmd: python src/prepare_data.py
    deps:
    - src/prepare_data.py
    outs:
    - data/iris.csv
  train:
    cmd: python src/train.py
    deps:
    - data/iris.csv
    - src/train.py
    outs:
    - models/model.joblib

Run the Pipeline and Commit:

dvc repro
git add DVC.yaml DVC.lock src/train.py
git commit -m "Add DVC pipeline for data prep and training"

Step 4: Containerization with Docker
Create the Prediction Service (app.py):
This Flask app will load the model and serve predictions.

import joblib
import pandas as pd
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# We assume the model will be present in the container
try:
    model = joblib.load('models/model.joblib')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file not found.")
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
        df = pd.DataFrame(json_)
        prediction = model.predict(df).tolist()
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

Create the Dockerfile:

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

Build and Test the Docker Image:

docker build -t mlops-service .
docker run -p 5000:5000 mlops-service

Your service is now running inside a container, accessible at http://localhost:5000.
