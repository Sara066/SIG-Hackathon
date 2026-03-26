import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def train_sentinel_brain():
    # 1. Load the augmented dataset
    data_path = 'data/metrics.csv'
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found. Run augment_data.py first!")
        return

    df = pd.read_csv(data_path)
    X = df[['mem_usage']]

    print(f"🧠 Training on {len(df)} samples...")

    # 2. Configure the Isolation Forest
    # n_estimators: 200 trees for a smoother decision boundary
    # contamination: 'auto' prevents the 0.57MB overfitting by calculating the threshold
    model = IsolationForest(
        n_estimators=200, 
        contamination=0.05, 
        random_state=42
    )

    # 3. Fit the model
    model.fit(X)

    # 4. Save the model for main.py to use
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/anomaly_model.pkl')
    
    print("✅ Success: 'models/anomaly_model.pkl' has been updated.")
    print("🚀 You can now run 'python main.py' to start the Sentinel.")

if __name__ == "__main__":
    train_sentinel_brain()