import joblib
import pandas as pd

# 1. Load the 'Brain'
model = joblib.load('models/anomaly_model.pkl')

def test_value(mem_mb):
    # Prepare the data in the same format it was trained (a DataFrame)
    test_data = pd.DataFrame([[mem_mb]], columns=['mem_usage'])
    
    # Predict: 1 = Normal, -1 = Anomaly
    prediction = model.predict(test_data)[0]
    
    status = "✅ NORMAL" if prediction == 1 else "🚨 ANOMALY"
    print(f"Testing RAM: {mem_mb}MB | Result: {status}")

# 2. Run the Test
print("--- KubeSentinel AI Validation ---")
test_value(0.65)   # A value from your normal idle time
test_value(500.0)  # A value from your 'dd' stress test