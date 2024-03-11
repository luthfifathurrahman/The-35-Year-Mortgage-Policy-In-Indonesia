# Initialize library
import pandas as pd
from pathlib import Path

# Set the maximum number of rows and columns to be displayed
pd.set_option('display.max_columns', None)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# Create a DataFrame
population_data_path = current_dir / "population_data.csv"
df = pd.read_csv(population_data_path, delimiter=',')

# Convert the data type of the "jumlah_penduduk" column to numeric
jumlah_penduduk = df.copy()
jumlah_penduduk['jumlah_penduduk'] = pd.to_numeric(jumlah_penduduk['jumlah_penduduk'])
print(jumlah_penduduk.info())
print(jumlah_penduduk)

# Saving to CSV file
output_dir = previous_dir / "datasets"
cleaned_population_data_path = output_dir / "cleaned_population_data.csv"
jumlah_penduduk.to_csv(cleaned_population_data_path, index=False)
