# PyDVC Docker MLOps Sandbox

## MLOps Local Project
This project serves as a hands-on, reproducible MLOps pipeline using key open-source tools. The goal is to demonstrate a complete machine learning workflow, from data versioning to containerized deployment, all on your local machine.## Key Features
- Python: The core language for data processing and model training.

- Git: Used for source code version control.

- DVC (Data Version Control): Manages and versions large datasets and models, keeping them separate from the Git repository.

- Docker: Containers the entire application for consistent, reproducible execution.


## Prerequisites
Before you begin, ensure you have the following installed on your system:


`Python 3.8+`

`Git`

`Docker`

`DVC (Data Version Control)`

## Project Structure
The project is organized into a clean and logical structure:

```
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

```
## Getting Started
Follow these steps to set up and run the project locally.

## Step 1: Project Setup

### 1. Initialize Git:

```
mkdir mlops-local-project
cd mlops-local-project
git init

```

### 2. Create Directories & Files:
Create the folder structure as shown above.


### 3.Setup Python Environment:

```
python -m venv venv
source venv/bin/activate
```

### 4.Install Dependencies:
Add the following to `requirements.txt`

```
scikit-learn
pandas
joblib
flask
gunicorn
dvc
```
Then, install them:
```
pip install -r requirements.txt
```

### 5. Configure .gitignore:
Add the following content to your .gitignore file:

venv/
__pycache__/
*.pyc
data/
models/
.env
.dvc/

## Step 2: Data Versioning with DVC

### 1.Initialize DVC:

```dvc init```

### 2.Create and Track Data:
Write a simple data preparation script in src/prepare_data.py.

Then, run the script and track the data with DVC and Git:

```
python src/prepare_data.py
dvc add data/iris.csv
git add data/iris.csv.dvc
git commit -m "Add iris dataset with DVC"

```
### 

## Step 3: Model Training and DVC Pipeline
### 1. Create the Training Script:
Write the training logic in src/train.py

### 2. Define the DVC Pipeline:
Create a DVC.yaml file to define the pipeline stages.

### 3.Run the Pipeline and Commit:
 
```
dvc repro
git add DVC.yaml DVC.lock src/train.py
git commit -m "Add DVC pipeline for data prep and training"

```

## Step 4: Containerization with Docker
### 1. Create the Prediction Service (app.py):
This Flask app will load the model and serve predictions.

### 2.Create the Dockerfile:
```
FROM python:3.13.5-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Build and Test the Docker Image:

```
docker build -t mlops-service .
docker run -p 5000:5000 mlops-service

```

Your service is now running inside a container, accessible at `http://localhost:5000`
