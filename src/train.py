import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import json

def train_model():
    """Trains a RandomForestClassifier and saves the model."""
    print("Starting model training...")
    # Load data from DVC-tracked path
    df = pd.read_csv('data/iris.csv')
    X = df.drop('target', axis=1)
    y = df['target']

    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Save the trained model
    joblib.dump(model, 'models/model.joblib')
    print("Model training complete. Model saved to models/model.joblib")

if __name__ == "__main__":
    train_model()