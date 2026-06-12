import pandas as pd

df = pd.read_csv("dataset/disease_data.csv")

print("Countries:")
print(df['country'].unique())

print("\nOccupations:")
print(df['occupation'].unique())