# Initialize library
import pandas as pd
import re
from pathlib import Path

# Set the maximum number of rows and columns to be displayed
pd.set_option('display.max_columns', None)

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
previous_dir = current_dir.parent

# Create a DataFrame
total_rumah_tangga_data_path = current_dir / "total_rumah_tangga_data.csv"
df_rt = pd.read_csv(total_rumah_tangga_data_path, delimiter=',')
df_rt = df_rt.rename(columns={'total': 'total_rt'})

kepemilikan_rumah_data_path = current_dir / "kepemilikan_rumah_data.csv"
df_pemilikan_rumah = pd.read_csv(kepemilikan_rumah_data_path, delimiter=',')
df_pemilikan_rumah = df_pemilikan_rumah.rename(columns={'total': 'total_rt_no_house'})

def process_string(df, column):
    # Define a function to remove number, dot and space at the beginning of a string
    # and capitalize the first letter of each word
    def process_string_in_row(s):
        s = re.sub(r'^\d+\.\s*', '', s)
        if s == 'DKI JAKARTA':
            return 'DKI Jakarta'
        elif s == 'DI YOGYAKARTA':
            return 'DI Yogyakarta'
        else:
            return s.title()

    # Apply the function to every row in the column
    df[column] = df[column].apply(process_string_in_row)

process_string(df_rt, 'provinsi')
process_string(df_pemilikan_rumah, 'provinsi')

# Join the two dataframes
df = pd.merge(df_pemilikan_rumah, df_rt, on='provinsi')
df['total_rt_have_house'] = df['total_rt'] - df['total_rt_no_house']

# Sorting the order of columns
sorted_column = ['provinsi',
                 'kontrak_sewa',
                 'bebas_sewa',
                 'lainnya',
                 'total_rt_no_house',
                 'total_rt_have_house',
                 'total_rt']
df = df[sorted_column]
print(df)

# Saving to CSV file
output_dir = previous_dir / "datasets"
cleaned_rumah_tangga_data_path = output_dir / "cleaned_rumah_tangga_data.csv"
df.to_csv(cleaned_rumah_tangga_data_path, index=False)
