import pandas as pd
import numpy as np

df = pd.read_csv('data/dataset_real_clean.csv')

df_clean = df.dropna()
print('Number of rows with NaN in the scenario:', df['scenario'].isna().sum())

df['scenario'] = df['scenario'].fillna('normal')

print('Unique scenario labels after cleaning:')
print(df['scenario'].unique())

df_clean.to_csv('data/dataset_real_clean.csv', index=False)
print(f"Deleted {len(df) - len(df_clean)} rows with NaN, remaining {len(df_clean)} clean rows.")
