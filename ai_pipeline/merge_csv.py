import pandas as pd

csv_files = ['normal.csv', 'high_temp.csv', 'low_light.csv', 'high_humidity.csv', 'anomaly.csv']

dfs = [pd.read_csv(f) for f in csv_files]
df_combined = pd.concat(dfs, ignore_index=True)

df_combined.to_csv('dataset_real.csv', index=False)
print("Combined CSV saved as dataset_real.csv")
