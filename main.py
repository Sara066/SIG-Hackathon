import docker
import time
import joblib
import pandas as pd
from models import AlertEvent
from healer.engine import fix_container

# 1. Load the 'Brain' once at the start
model = joblib.load('models/anomaly_model.pkl')
client = docker.from_env()

def run_sentinel():
    target = "sentinel-db"
    print(f"--- KubeSentinel v0.5: AI-POWERED ---")
    
    while True:
        try:
            container = client.containers.get(target)
            stats = container.stats(stream=False)
            mem = stats['memory_stats']['usage'] / (1024 * 1024)
            
            # 2. ASK THE AI: "Is this weird?"
            test_df = pd.DataFrame([[mem]], columns=['mem_usage'])
            prediction = model.predict(test_df)[0] # 1 = Normal, -1 = Anomaly
            
            status_icon = "✅" if prediction == 1 else "⚠️"
            print(f"SCAN: {target} | RAM: {mem:.2f}MB | AI Status: {status_icon}")

            # 3. AI-BASED HEALING
            if prediction == -1:
                print(f"🤖 AI DETECTED ANOMALY! Predicted Memory Exhaustion.")
                fix_container(target)
                print("Waiting for cooldown...")
                time.sleep(10) # Give it time to restart

        except Exception as e:
            print(f"System Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    run_sentinel()