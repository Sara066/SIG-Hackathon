import pandas as pd
import numpy as np

# Load your current data
df = pd.read_csv('data/metrics.csv')

# Create 100 rows of "Normal-ish" data between 0.4MB and 1.5MB
fake_normal = pd.DataFrame({
    'timestamp': [0]*100,
    'mem_usage': np.random.uniform(0.4, 1.5, 100) 
})

# Combine and save
new_df = pd.concat([df, fake_normal])
new_df.to_csv('data/metrics.csv', index=False)
print("Dataset expanded! Now re-run your training script.")