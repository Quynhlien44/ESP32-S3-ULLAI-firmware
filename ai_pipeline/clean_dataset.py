import pandas as pd

df = pd.read_csv('dataset_real.csv')


print('Number of rows with NaN in the scenario:', df['scenario'].isna().sum())

df['scenario'] = df['scenario'].fillna('normal')

print('Unique scenario labels after cleaning:')
print(df['scenario'].unique())

df.to_csv('dataset_real_clean.csv', index=False)
print("Saved cleaned dataset to dataset_real_clean.csv")
