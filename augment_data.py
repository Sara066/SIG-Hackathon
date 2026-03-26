import pandas as pd
import numpy as np

# Create a realistic "Normal" dataset
# This tells the AI that anything between 0.4MB and 2.0MB is SAFE
normal_data = pd.DataFrame({
    'timestamp': range(500),
    'mem_usage': np.random.uniform(0.4, 1.5, 500) 
})

# Save as a fresh file
normal_data.to_csv('data/metrics.csv', index=False)
print("✅ Baseline Reset: Normal range defined as 0.4MB - 1.5MB.")