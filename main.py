import docker
import time
import joblib
import pandas as pd
import shap
import os
from healer.engine import fix_container

# 1. Initialize the 'Brain' and Explainability Layer
def initialize_sentinel():
    try:
        # Load the trained Isolation Forest model
        model_path = 'models/anomaly_model.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        model = joblib.load(model_path)
        
        # Define a prediction wrapper for SHAP
        # Isolation Forest 'decision_function' tells us how 'normal' a point is
        def model_predict(data):
            return model.decision_function(data)

        # Create a Kernel Explainer using a reference 'normal' value (1.0 MB)
        # This bypasses the TreeExplainer index errors for 1-feature models
        background_data = pd.DataFrame([[1.0]], columns=['mem_usage'])
        explainer = shap.KernelExplainer(model_predict, background_data)
        
        client = docker.from_env()
        return model, explainer, client
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        print("Tip: Run 'python augment_data.py' and 'python train.py' first.")
        exit(1)

def run_sentinel():
    model, explainer, client = initialize_sentinel()
    target = "sentinel-db"
    
    print(f"\n--- KubeSentinel v1.2: AI + Stable SHAP ---")
    print(f"Monitoring Target: {target}\n")
    
    while True:
        try:
            # 2. Scrape Live Telemetry via Docker SDK
            container = client.containers.get(target)
            stats = container.stats(stream=False)
            
            # Convert bytes to MB
            mem_mb = stats['memory_stats']['usage'] / (1024 * 1024)
            
            # 3. AI Inference: Check for Anomalies
            test_df = pd.DataFrame([[mem_mb]], columns=['mem_usage'])
            prediction = model.predict(test_df)[0] # 1 = Normal, -1 = Anomaly
            
            status_icon = "✅" if prediction == 1 else "⚠️"
            print(f"SCAN: {target} | RAM: {mem_mb:.2f}MB | AI Status: {status_icon}")

            # 4. Autonomous Healing with Explainability
            if prediction == -1:
                # Calculate SHAP values (KernelExplainer returns a list of arrays)
                shap_values = explainer.shap_values(test_df)
                mem_impact = float(shap_values[0][0]) # Impact of the single RAM feature
                
                print(f"\n🚨 [AI ALERT] ANOMALY DETECTED!")
                print(f"🤖 Reasoning: RAM deviation impact score is {mem_impact:.4f}")
                print(f"🛠️  Action: Executing Proactive Self-Healing...")
                
                # Trigger the Healer (logs to audit_log.txt)
                fix_container(target)
                
                print("Waiting for cooldown (10s)...")
                time.sleep(10) 
                print("Sentinel Resuming Scan...\n")

        except docker.errors.NotFound:
            print(f"Error: Container '{target}' not found. Ensure 'docker-compose up -d' is running.")
        except Exception as e:
            print(f"Loop Error: {e}")
        
        # Telemetry interval (2 seconds as per README)
        time.sleep(2)

if __name__ == "__main__":
    run_sentinel()