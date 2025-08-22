import pandas as pd
import json

df = pd.read_csv('data/dataset_real_clean.csv')
def safe_std(x):
    s = x.std()
    return s if s > 1e-5 else 1.0   # Avoid zero std to prevent division by zero

scaler = {
    'ldr_min': float(df['ldr_v'].min()),
    'ldr_max': float(df['ldr_v'].max()),
    'tvoc_min': float(df['tvoc_ppb'].min()),
    'tvoc_max': float(df['tvoc_ppb'].max()),
    'eco2_min': float(df['eco2_ppm'].min()),
    'eco2_max': float(df['eco2_ppm'].max()),
    'temp_mean': float(df['temp_c'].mean()),
    'temp_std': safe_std(df['temp_c']),
    'hum_mean': float(df['hum_pct'].mean()),
    'hum_std': safe_std(df['hum_pct']),
}

with open('scaler.json', 'w') as f:
    json.dump(scaler, f)
print("Scaler saved to scaler.json")
