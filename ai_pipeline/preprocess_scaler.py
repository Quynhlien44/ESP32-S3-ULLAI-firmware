import pandas as pd
import json

df = pd.read_csv('dataset_real_clean.csv')
scaler = {
    'ldr_min': float(df['ldr_v'].min()), 'ldr_max': float(df['ldr_v'].max()),
    'tvoc_min': float(df['tvoc_ppb'].min()), 'tvoc_max': float(df['tvoc_ppb'].max()),
    'eco2_min': float(df['eco2_ppm'].min()), 'eco2_max': float(df['eco2_ppm'].max()),
    'temp_mean': float(df['temp_c'].mean()), 'temp_std': float(df['temp_c'].std()),
    'hum_mean': float(df['hum_pct'].mean()), 'hum_std': float(df['hum_pct'].std())
}
with open('scaler.json', 'w') as f:
    json.dump(scaler, f)
print("Scaler saved to scaler.json")
