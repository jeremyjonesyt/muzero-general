import pandas as pd

log_path = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2\experiment_results.csv'

# Load the file
df = pd.read_csv(log_path, header=None)

print("--- First 5 rows of data ---")
print(df.head())
print("\n--- Data types for each column ---")
print(df.dtypes)
