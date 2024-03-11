# Initialize library
import pandas as pd
from pathlib import Path

# Set the maximum number of rows and columns to be displayed
pd.set_option('display.max_columns', None)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# Create a DataFrame
ump_data_path = current_dir / "ump_data.csv"
df_ump = pd.read_csv(ump_data_path, delimiter=',')

# Altering column names using the rename method.
df = df_ump.copy()
df = df.rename(columns={'upah minimum provinsi': 'ump'})

# Remove "," from each value in the "ump" column
df['ump'] = df['ump'].str.replace(',', '')

# Convert the data type into float
df['ump'] = df['ump'].astype(float)

df['provinsi'] = df['provinsi'].replace('DI. Yogyakarta', 'DI Yogyakarta')

# Adding a new column with identical values (value=1620000)
df['rata_rata_angsuran'] = 1620000
print(df)

# Saving to CSV file
output_dir = previous_dir / "datasets"
cleaned_ump_data_path = output_dir / "cleaned_ump_data.csv"
df.to_csv(cleaned_ump_data_path, index=False)
