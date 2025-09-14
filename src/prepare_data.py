import pandas as pd
from sklearn.datasets import load_iris
import os

def prepare_data():
    """Loads the iris dataset and saves it to a CSV."""
    print("Preparing data...")
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    # Load dataset
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target

    # Save the dataset to be tracked by DVC
    df.to_csv('data/iris.csv', index=False)
    print("Data preparation complete.")

if __name__ == "__main__":
    prepare_data()
