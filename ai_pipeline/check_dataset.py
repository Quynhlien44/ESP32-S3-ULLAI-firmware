import pandas as pd

df = pd.read_csv('dataset_real.csv')

print("Unique scenario labels in dataset:")
print(df['scenario'].unique())

print("\nNumber of samples per scenario:")
print(df['scenario'].value_counts())

print("\nSample data preview:")
print(df.head())
