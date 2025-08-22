import pandas as pd
import numpy as np

df = pd.read_csv('data/dataset_real_clean.csv')

print("Check for NaN in columns:")
print(df.isna().sum())

print("\nCheck for max/min values:")
print(df.describe())

print("\nCheck for Inf values in the data:")
print(np.isinf(df.values).sum())
