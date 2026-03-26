import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_model():
    # 1. Load the data
    if not os.path.exists('data/metrics.csv'):
        print("Error: No data found in data/metrics.csv. Run main.py first!")
        return
        
    df = pd.read_csv('data/metrics.csv')
    
    # 2. Prepare the feature (Memory Usage)
    # Isolation Forest looks for 'outliers' in this column
    X = df[['mem_usage']] 

    # 3. Train the Model
    # contamination=0.1 means we expect 10% of the data to be 'weird' (your stress test)
    model = IsolationForest(contamination=0.1, random_state=42)
    print("🤖 Training Isolation Forest model...")
    model.fit(X)
    
    # 4. Save the 'Brain'
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, 'models/anomaly_model.pkl')
    print("✅ Success! Model saved to models/anomaly_model.pkl")

if __name__ == "__main__":
    train_model()