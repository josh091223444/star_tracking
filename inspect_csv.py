import pandas as pd

df = pd.read_csv("Star_tracking.csv")
print("\n--- HEAD ---")
print(df.head())

print("\n--- TAIL ---")
print(df.tail())

print("\n--- UNIQUE TIMES ---")
print(df["Time"].unique())

print("\n--- BODY COUNTS ---")
print(df["Body"].value_counts())
